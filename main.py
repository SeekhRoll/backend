import psycopg2

# Connect to the PostgreSQL server
connection = psycopg2.connect(database='postgres', user='postgres', password='HeeHaw', host='localhost', port='5432') # do this on heroku?

# Create a new database
connection.autocommit = True
cursor = connection.cursor()
cursor.execute("CREATE DATABASE metal_db;")
cursor.close()
connection.close()