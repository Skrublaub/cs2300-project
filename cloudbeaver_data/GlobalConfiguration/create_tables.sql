create table Player (
  Speed int NOT NULL,
  Max_Health int NOT NULL,
  Current_Health int NOT NULL,
  Experience int NOT NULL,
  Player_Level int NOT NULL,
  Character_Name text NOT NULL CHECK (Character_Name <> ''),

  -- Since ability scores are generally in order, the array can be standardized
  -- Str, Dex, Con, Int, Wis, and Cha respectively for every index in each Ability_Score value
  -- The standard array of [15, 14, 13, 12, 10, 8] would be
  -- 15 Str, 14 Dex, 13 Con, 12 Int, 10 Wis, and 8 Cha
  -- Saves the hassle of making a new table in the db just to keep track of Ability Scores
  Ability_Scores int[] NOT NULL,
  ID int PRIMARY KEY,
  CHECK (Max_Health > 0 AND Current_Health > 0 AND Player_Level > 0 AND Player_Level <= 20 AND Experience >= 0)
);
