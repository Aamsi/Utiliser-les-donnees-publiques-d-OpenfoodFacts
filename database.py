import mysql.connector
from mysql.connector import errorcode

from create_tables import TABLES

cnx = mysql.connector.connect(host='localhost', user='student_P5', password='studentOC97')
cursor = cnx.cursor()

cursor.execute("USE openfoodfacts_P5")
for table in TABLES:
    try:
        cursor.execute(table)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg) 

cursor.execute("SHOW TABLES")

for i in cursor:
    print(i)

cnx.close()