# Sean Summers Assignment 7.2
# This program will let the user update and delete records in the database.


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

    # create the cursor object
    cursor = db.cursor()

    def show_films(cursor, title):
        # method to execute an inner join on all tables,
        # iterate over the dataset and output the results to the terminal window.

        # inner join query
        cursor.execute(
            "select film_name as Name, film_director as Director, genre_name as Genre, " \
            "studio_name as 'Studio Name' from film INNER JOIN genre on " \
            "film.genre_id = genre.genre_id INNER JOIN studio on film.studio_id = studio.studio_id;")
        
        # get the results from the cursor object
        films = cursor.fetchall()

        print("\n -- {} --".format(title))

        # iterate over the film data set and display the results
        for film in films:
            print("Film Name: {} \nDirector: {} \nGenre Name ID: {} \nStudio Name: {} \n".format(film[0], film[1], film[2], film[3]))

    # display the films
    show_films(cursor, "DISPLAYING FILMS")

    # insert a new record into the film table
    cursor.execute(
        "INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)"\
        "   VALUES ('Oppenheimer', '2023', '180', 'Christopher Nolan', '3', '3')"
        )

    # display the films after the insert
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # update Alien to have the horror genre
    cursor.execute(
        "UPDATE film SET genre_id = '1' WHERE film_name = 'Alien'"
        )
    
    # display the films after the update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

    # delete the Gladiator record
    cursor.execute(
        "DELETE FROM film where film_name = 'Gladiator'"
        )
    
    # display the films after the delete
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
    



 
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
