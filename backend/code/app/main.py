from fastapi import FastAPI, Request , HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg as ps
from psycopg.rows import dict_row
from typing import Optional, Final
import secrets
import hashlib
from json2html import *

app = FastAPI(root_path="/api", docs_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

authorization: list[str] = ["ed72ba2a2ce8cc774f01e3e9c721f929"]

table_keys: dict[str, str] = {
    "weapons": "weapon_name",
    "armor": "armor_name",
    "class": "class_name",
    "tools": "tool_name",
    "background": "bg_name",
    "spells": "spell_name",
    "skills": "skill_name",
    "monsters": "monster_name",
    "monster_actions": "action_name",  # this one is gonna need a monster part in the form as well
    "languages": "language_name",
    "race": "race_name",
    "admins": "username"
}

adjacent_tables: dict[str, list[str]] = {
    "weapons": ["can_use_weapon"],
    "armor": ["can_wear"],
    "class": ["can_wear", "can_use_weapons", "can_use_tool", "class_skills", "class_can_cast"],
    "tools": ["can_use_tool", "background_tools"],
    "background": ["background_tools", "background_langs", "background_skills"],
    "spells": ["class_can_cast"],
    "skills": ["background_skills", "class_skills", "monster_skills"],
    "monsters": ["monster_lang", "monster_skills", "monster_actions"],
    "monster_actions": ["monsters"],
    "languages": ["background_langs", "race_languages", "monster_lang"],
    "race": ["race_languages"],
}

allowed_agg_operators: Final[list[str]] = [
    ">",
    "<",
    "<=",
    ">=",
    "="
]

allowed_agg_funcs: Final[list[str]] = ["AVG", "COUNT", "MAX", "MIN", "SUM"]


async def execute_query(q_str: str, as_dict: bool = False) -> Optional[list]:
    """
    Runs a query on the postgres database.

    Parameters:
        q_str (str): The query string that is to be ran on the database
        as_dict (bool): Determines whether or not the query result is to be
            returned in list form or dictionary form.
            If True, row_factory is set to dict_row instead of the default
            If False, row_factory is lest untouched

    Raises:
        HTTPException (400): If the query failed for some reason, this is raised
            and returned to the user

    Returns:
        List or Dict: if the query returns tuples
        None: If the query returns no list or tuples
    """
    cur_args: dict = {}
    if as_dict:
        cur_args["row_factory"] = dict_row

    async with await ps.AsyncConnection.connect(dbname="root", user="root", host="172.69.0.4") as conn:
        async with conn.cursor(**cur_args) as cur:
            try:
                await cur.execute(q_str)
            except ps.Error:
                return HTTPException(400, "The sql query failed. Please correct query or contact server admin")

            if cur.description is not None:
                return await cur.fetchall()
            
            return None
        

async def check_headers(headers: dict) -> HTTPException | None:
    """
    Checks to see if an auth token is present in
    a passed headers dictionary.
    """
    if "authorization" not in headers.keys():
        return HTTPException(401, "No Authorization header passed")

    if headers["authorization"] not in authorization:
        return HTTPException(401, "Bad Authorization token")
    
    return
    

@app.put("/login/")
async def create_user(request: Request):
    """
    Creates a user in the database for logging in/out.
    Takes a password in and hashes it.

    Form data:
        username (str): username to create
        password (str): password to create
        admin_key (str): The super secret password
            that is unguessable good luck and
            godspeed
    """
    async with request.form() as form:
        data = dict(form)

    for item in ("username", "password", "admin_key"):
        if item not in data.keys():
            return HTTPException(400, "Bad request lmao good luck figuring the secret out")

    if data["admin_key"] != "Br()NoLmao":
        return HTTPException(400, "Bad admin_key lol")
    
    check_query: str = f"SELECT username FROM admins"
    ret_data = await execute_query(check_query)
    for item in ret_data:
        if item[0] == data["username"]:
            return HTTPException(400, "ERROR: Username already exists")
    
    pw_salt: str = secrets.token_hex(32)
    total_pw: str = data["password"] + pw_salt
    hash = hashlib.sha256(total_pw.encode())
    hash_str: str = hash.hexdigest()

    sql_string: str = f"INSERT INTO admins VALUES ('{data['username']}', '{hash_str}', '{pw_salt}')"

    ret_data = await execute_query(sql_string)
    if isinstance(ret_data, HTTPException):
        return ret_data

    return HTTPException(200, "User Created")


@app.get("/login/")
async def login(request: Request):
    """
    Logs a user in and returns a 16 character token
    hex as an authorization cookie.

    Form data:
        username (str): The username to login with
        password (str): The password idk what else to say
    """
    async with request.form() as form:
        data = dict(form)

    for item in ("username", "password"):
        if item not in data.keys():
            return HTTPException(400, "Invalid Form data sent")
        
    ret_data = await execute_query(f"SELECT * FROM admins WHERE username = '{data['username']}'")
    if isinstance(ret_data, HTTPException):
        return ret_data

    pw_salt: str = ret_data[0][2]
    hash_str: str = hashlib.sha256(f"{data['password']}{pw_salt}".encode()).hexdigest()
    
    if hash_str == ret_data[0][1]:
        temp_auth_token: str = secrets.token_hex(16)
        authorization.append(temp_auth_token)
        return HTTPException(200, "Login Success", {"Authorization": temp_auth_token})
    
    return HTTPException(401, "Login failed lol")


@app.get("/logout/")
async def user_logout(request: Request):
    """
    Logs a user out of their account.
    What it really does is remove an index from
    the authorization list.
    """
    ret_data = await check_headers(request.headers)
    if isinstance(ret_data, HTTPException):
        return ret_data
    
    idx: int = authorization.index(request.headers["authorization"])
    authorization.pop(idx)

    return HTTPException(200, "User logged out")


@app.get("/search/{table}/")
async def search(table: str, search_term: str | None = None):
    """
    Searches a specific table for a value.
    Can only search by primary key which all primary keys in this database are strings.
    """
    if search_term is None:
        return HTMLResponse(400, "Send parameter search_term please")

    search_term = str(search_term)
    
    prim_key: str = table_keys[table]

    sql_string: str = f"SELECT * FROM {table} WHERE {prim_key} LIKE '%{search_term}%'"
    sql_response = await execute_query(sql_string, as_dict=True)

    if table == "monsters":
        for monster in sql_response:
            extra_sql: str = f"SELECT action_name FROM {table} NATURAL JOIN monster_actions WHERE {prim_key} LIKE '%{monster['monster_name']}%';"
            extra_response = await execute_query(extra_sql)
            if isinstance(extra_response, HTTPException):
                return extra_response
    
            monster["actions"] = []
            for action in extra_response:
                monster["actions"].append(action[0])
    
    return sql_response


@app.get("/search_html/{table}/", response_class=HTMLResponse)
async def search_html(table: str | int, search_term: str | None = None):
    """
    Same as /search/ but returns an hmtl table rather
    than json.
    """
    json_response = await search(table, search_term)
    return json2html.convert(json=json_response)

    
@app.post("/insert/")
async def insert(table: str | None, request: Request):
    """
    Creates a tuple inside of the database

    Form data:
        The form data for this one is a bit different.
        The data passed will correspond with the
        row and value to add to that row.
        For example: If I wanted to add a skill named "Chug"
        with the related ability "Con", I would pass
        -F skill_name=Chug -F related_ability=Con
        with the curl command.
    """
    check_val = await check_headers(request.headers)
    if check_val is not None:
        return check_val

    if table is None:
        raise HTTPException(400, "table required")
    
    async with request.form() as form:
        data = dict(form)
        
    sql_string = f"INSERT INTO {table} ("
    for key in data.keys():
        temp_str: str = f"{key},"
        sql_string += temp_str

    sql_string = sql_string[:-1] + ") "
    sql_string += "VALUES ("

    for value in data.values():
        sql_string += f"'{value}',"

    sql_string = sql_string[:-1] + ")"

    ret_data = await execute_query(sql_string)
    if isinstance(ret_data, HTTPException):
        return ret_data

    return HTTPException(200, "Updated Successfully")


@app.patch("/insert/")
async def insertp(table: str | None, request: Request):
    """
    This function updates a tuple in the database with new values.
    Works with primary keys only.
    
    Form data:
        col_name (str): The column that is to be modified
        new_val (str | int): The new value to change to
        prim_key_value (str | int): The primary key of the tuple to change
    """
    check_val = await check_headers(request.headers)
    if check_val is not None:
        return check_val  # returns an html header
    
    if table is None:
        raise HTTPException(400, "table required")
    
    async with request.form() as form:
        data = dict(form)

    prim_key: str = table_keys[table]
  
    try:
        sql_string: str = f"UPDATE {table} SET {data['col_name']} = '{data['new_val']}' WHERE {prim_key} = '{data['prim_key_val']}'"
    except:
        return HTTPException(400, "not all columns passed properly")

    ret_data = await execute_query(sql_string)
    if isinstance(ret_data, HTTPException):
        return ret_data

    return HTTPException(200, "Updated Successfully")


@app.delete("/delete/")
async def delete(request: Request):
    """
    This function deletes a tuple from a table

    Items needed in form data:
        table (str): The table to drop data from
        col_name (str): The column to drop find a value to drop from
        drop_val (str): The value to drop from the table
    """
    check_val = await check_headers(request.headers)
    if check_val is not None:
        return check_val
    
    async with request.form() as form:
        data = dict(form)

    try:
        sql_string: str = f"DELETE FROM {data['table']} WHERE {data['col_name']} = '{data['drop_val']}'"
    except:
        return HTTPException(400, "failed request")
    
    ret_data = await execute_query(sql_string)
    if isinstance(ret_data, HTTPException):
        return ret_data

    return HTTPException(200, "Updated Successfully")


@app.get("/stat/{table}/")
async def table_stat(table: str, request: Request):
    """
    This function runs a selected aggregate function on 
    a table in a database and returns it.

    Items needed in form data:
        col_name (str): The name of the column to run the aggregate functions on
        agg_func (str): The type of aggregate function to run on the table
            Only AVG, COUNT, MAX, MIN, SUM are allowed
        condition (str | int | None): Condition to check the values of. Type must be
            the same as condition_val.            
            Only >, <, >=, <=, = are allowed
        condition_val (str | int | None): Condition value to test for. Type must be the
            same as condition.
        group_col (str | None): The column to run the groub by method through 
    """
    async with request.form() as form:
        data = dict(form)

    for key in data.keys():
        if key not in ("col_name", "agg_func", "condition", "condition_val", "group_col"):
            return HTTPException(400, "Form data invalid")

    if "col_name" not in data.keys():
        return HTTPException(400, "No col_name form data found")
    
    if "agg_func" not in data.keys():
        return HTTPException(400, "No agg_func form data found")

    if data["agg_func"].upper() not in allowed_agg_funcs:
        return HTTPException(400, "Bad agg_func") 

    if "condition" in data.keys():    
        if data["condition"] not in allowed_agg_operators:
            return HTTPException(400, "Incorrect condition")
    
    if data["agg_func"] not in allowed_agg_funcs:
        return HTTPException(400, "Incorrect agg_func")
        
    sql_query: str = f"SELECT {data['agg_func']}({data['col_name']}) FROM {table} "
    
    if "condition" in data.keys() and "condition_val" in data.keys():
        sql_query += f"WHERE {data['col_name']} {data['condition']} {data['condition_val']} "
    if "group_col" in data.keys():
        sql_query += f"GROUP BY {data['group_col']}"

    ret_data = await execute_query(sql_query)
    
    return ret_data