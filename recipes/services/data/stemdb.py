import sqlite3
import json
import re

#
# Snowball stemmer is a proper stemmer for Dutch Language
#

import snowballstemmer
stemmer = snowballstemmer.stemmer('dutch');

conn = sqlite3.connect('./db/ingredients_stemmed_snowball.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS ingredients
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, stemmed_name text)''')

c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS name_uniq_idx ON ingredients (name)''')

# Save (commit) the changes
conn.commit()

with open('./../../notebook/recipes.json', 'r') as json_lines_file:
    json_recipes = [json.loads(line.strip()) for line in json_lines_file.readlines()]

ingredSet = set()
for doc in json_recipes:
    # Insert a row of data
    for ingredient in doc['ingredient_search_terms']:
        stem = stemmer.stemWord(ingredient)
        ingredSet.add(ingredient + ':' + stem)
        c.execute('INSERT OR IGNORE INTO ingredients (name,stemmed_name) VALUES (?,?)', (ingredient, stem))

for elem in ingredSet:
    print(elem)

# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

# er/es/e/s/ant
