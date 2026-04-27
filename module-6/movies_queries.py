""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values

# using our .env file 
secrets = dotenv_values(".env")
 
""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """ 
 
    db = mysql.connector.connect(**config) # connect to the movies database 
    
    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
 
    input("\n\n  Press any key to continue...")

    """ Create a cursor and query the database. """
    cursor = db.cursor()
    print("\n  -- DISPLAYING Studio RECORDS --")
    cursor.execute("select * from studio")
    for row in cursor:
        print(f" Studio ID: {row[0]} \n Studio Name: {row[1]}")
        print("\n")

    print("\n  -- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre")
    for row in cursor:
        print(f" Genre ID: {row[0]} \n Genre Name: {row[1]}")
        print("\n")

    print("\n  -- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    for row in cursor:
        print(f" Film Name: {row[0]} \n Runtime: {row[1]}")
        print("\n")

    print("\n  -- DISPLAYING Film DIRECTORS in ORDER --")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    for row in cursor:
        print(f" Film Name: {row[0]} \n Director: {row[1]}")
        print("\n")
    cursor.close() # close the cursor



 
except mysql.connector.Error as err:
    """ on error code """
 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
 
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
 
    else:
        print(err)
 
finally:
    """ close the connection to MySQL """
 
    db.close()


