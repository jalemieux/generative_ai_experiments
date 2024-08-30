
import sqlite3

conn = sqlite3.connect('characters.db')
c = conn.cursor()
#c.execute('''DROP TABLE IF EXISTS characters''')
c.execute('''CREATE TABLE characters
             (name TEXT, age INTEGER, gender TEXT, physical_description TEXT, personality_traits TEXT, image TEXT, unique_features TEXT)''')


#c.execute('''DROP TABLE IF EXISTS stories''')
c.execute('''CREATE TABLE stories
             (description TEXT, supporting_characters TEXT, antagonists TEXT, plot TEXT, lessons TEXT)''')
conn.commit()
conn.close()