# Create an Account:
Run twice to show user already exists:

`curl -L -X PUT https://cs2300.skrublaub.xyz/api/login/ -F username=tempuser -F password=temppassword -F "admin_key=Br()NoLmao"`

# Login:
This one should fail:

`curl -L -X GET https://cs2300.skrublaub.xyz/api/login/ -F username=nologin -F password=nopassword`

This one should succeed:

`curl -L -X GET https://cs2300.skrublaub.xyz/api/login/ -F username=ratl -F password=baller`

To save auth token:

`export auth="Authorization: token"`

In case of auth token failure failure for some reason:

`export auth="Authorization: ed72ba2a2ce8cc774f01e3e9c721f929"`

# Search:
`curl -L -X GET https://cs2300.skrublaub.xyz/api/search/monsters/?search_term=Archer`

`curl -L -X GET https://cs2300.skrublaub.xyz/api/search/spells/?search_term=H`

# Create tuple(s):
Show that user needs an auth token to create a tuple:

`curl -X POST https://cs2300.skrublaub.xyz/api/insert/?table=skills -F skill_name=Chug -F related_ability=Con`

Now create a value in the table:

`curl -X POST -H "$auth" https://cs2300.skrublaub.xyz/api/insert/?table=skills -F skill_name=Chug -F related_ability=Con`

Another create example to show off the mutiple input support:

`curl -X POST -H "$auth" https://cs2300.skrublaub.xyz/api/insert/?table=languages -F language_name=carnish -F language_type="" -F language_script="common" -F book_source="RoeBook" -F typical_speakers="{Humans, Gnomes}"`

# Modify tuple(s):

Modify the Chug tuple made in skills just now:

`curl -X PATCH -H "$auth" https://cs2300.skrublaub.xyz/api/insert/?table=skills -F col_name=related_ability -F new_val=Wis -F prim_key_val=Chug`

# Delete tuples(s):

Delete the Chug tuple from the database:

`curl -L -X DELETE -H "$auth" "https://cs2300.skrublaub.xyz/api/delete/" -F table=skills -F col_name=skill_name -F drop_val=Chug`

# Logout:

Logout of the current session and run twice:

`curl -L -X GET -H "$auth" https://cs2300.skrublaub.xyz/api/logout/`

# Stat:
`curl -L -X GET https://cs2300.skrublaub.xyz/api/stat/monsters/ -F col_name=hit_points -F agg_func=SUM`

`curl -L -X GET https://cs2300.skrublaub.xyz/api/stat/monsters/ -F col_name=hit_points -F agg_func=SUM -F condition=">=" -F condition_val=20`

`curl -L -X GET https://cs2300.skrublaub.xyz/api/stat/monsters/ -F col_name=hit_points -F agg_func=SUM -F condition=">=" -F condition_val=20 -F group_col=alignment`

`curl -L -X GET https://cs2300.skrublaub.xyz/api/stat/monsters/ -F col_name=hit_points -F agg_func=SUM -F group_col=monster_size`

`curl -L -X GET https://cs2300.skrublaub.xyz/api/stat/monsters/ -F col_name=hit_points -F agg_func=AVG -F group_col=monster_size`