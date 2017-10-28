#!/usr/bin/env python3

''' A small program that creates a simple SQLite3 database. Creates tables      
and puts some sample data into the tables.

NOTE:
This is a run-once program. If ran a second time, it will fail at the table 
creation statements.

'''
#!/usr/bin/env python3
# File Name: recipe_database_creator.py

''' A small program that creates a simple SQLite3 database. Creates tables 
and puts some sample data into the tables.

This is a run-once program. If ran a second time, it will fail at the table 
creation statements.
TODO: Wrap it in a try..catch handler to handle errors when script is re-used"
'''

import apsw     # SQLite3 Wrapper

# create/open connection to DB
connection = apsw.Connection("recipe_app.db")
cursor = connection.cursor()

# create Recipe table - Holds gross recipe information
sql = 'CREATE TABLE Recipes(pkid INTEGER PRIMARY KEY, name TEXT, servings \
        TEXT, source TEXT)'
cursor.execute(sql)

# Create Instructions table - Holds instructions for each recipe
sql = 'CREATE TABLE Instructions(pkid INTEGER PRIMARY KEY, recipeID NUMERIC, \
instructions TEXT)'
cursor.execute(sql)

# Create Ingredients table - holds a list of ingredients for each recipe
sql = 'CREATE TABLE Ingredients(pkid INTEGER PRIMARY KEY, recipeID NUMERIC, \
ingredients TEXT)'
cursor.execute(sql)

# Add Sample Data into Recipe Table
sql = 'INSERT INTO Recipes(name, servings, source) VALUES("Pasta with bacon and tomato sauce", 3, "Arthur Ngondo")'
cursor.execute(sql)

# Get value assigned to last pkID in Recipe Table
sql = 'SELECT last_insert_rowid()'
cursor.execute(sql)
for x in cursor.execute(sql):
    lastid = x[0]

# Add sample data into Instructions Table
sql = 'INSERT INTO Instructions(recipeID, instructions) VALUES({}, "Cut the onion, red peppers and bacon into small pieces. Heat some olive oil in a pan and fry the onion, red pepper and bacon. Add oregano, garlic, tomatoes and water and cook for 20 minnutes. Cook the pasta in a big pot of boiling water. Serve the pasta with tthe sauce.")'.format(
    lastid)
cursor.execute(sql)

# Add sample data into Ingredients table
sql = 'INSERT INTO Ingredients(recipeID, ingredients) VALUES ({}, "1 red onion. 2 red peppers. 120g bacon. 1 can (450g) tomatoes. 1 cup water. olive oil. garlic. oregano 50g pasta per person")'.format(lastid)
cursor.execute(sql)

# Add Sample Data into Recipe Table
sql = 'INSERT INTO Recipes(name, servings, source) VALUES("Spanish Rice", 4, \
"Greg Walters")'
cursor.execute(sql)

# Get value assigned to last pkID in Recipe Table
sql = 'SELECT last_insert_rowid()'
cursor.execute(sql)
for x in cursor.execute(sql):
    lastid = x[0]

# Add sample data into Instructions Table
sql = 'INSERT INTO Instructions(recipeID, instructions) VALUES({}, "Brown \
hamburger. Stir all other ingredients. Bring to a boil. Stir. Lower-to simmer.\
Cover and cook for 20 minutes or untill all liquid is absorbed.")'.format(
    lastid)
cursor.execute(sql)

# Add sample data into Ingredients table
sql = 'INSERT INTO Ingredients(recipeID, ingredients) VALUES ({}, "1 cup \
parboiled Rice (uncooked). Nyanya, Royco, Spices.")'.format(lastid)
cursor.execute(sql)