from mysql import connector

connection = connector.connect(
    host = "localhost",
    user = "root",
    password = "blabla",
    database = "spor"
    )
cursor = connection.cursor()