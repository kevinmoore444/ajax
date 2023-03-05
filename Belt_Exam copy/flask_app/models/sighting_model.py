from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash
import re

# Creating a Sighting "class". One user can have many sightings.

class Sighting:
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.sighting_date = data['sighting_date']
        self.number_of = data['number_of']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# Class methods are functions which can be invoked on the controller file. 

#This function joins the users and sightings in SQL and packages all the data together 
#so that the info can be displayed on an html. Database variable is defined in the init.py file.


    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM sightings 
            JOIN users ON sightings.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_sightings = []
        if results:
            for row in results:
                this_sighting = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                this_user = user_model.User(user_data)
                this_sighting.reporter = this_user
                all_sightings.append(this_sighting)
        return all_sightings

# This function joins users and sightings and filters for one particular sighting. The id is passed in via
# the data dictionary, which is supplied via the route which invokes this function. cls is also invoked
# in the route.

    @classmethod
    def get_one(cls,data):
        query = """
            SELECT * FROM sightings JOIN users
            ON users.id = sightings.user_id
            WHERE sightings.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:    
            one_sighting = cls(results[0])
            row = results[0]
            user_data = {
                    **row,
                    "id" : row['users.id'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at'],
            }
            user_instance = user_model.User(user_data)
            one_sighting.reporter = user_instance
            return one_sighting
        return False

# Create a new sighting and insert it into the SQL database. These values are supplied in an html form,
# then passed through a route in the controller, then passed from here into SQL

    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO sightings (location, what_happened, sighting_date, number_of, user_id)
            VALUES (%(location)s,%(what_happened)s,%(sighting_date)s,%(number_of)s, %(user_id)s)
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# Update a pre-existing sighting. Similar to create except different SQL query. Data dictionary passed via
# the route.

    @classmethod
    def update(cls,data):
        query = """
            UPDATE sightings 
            SET location = %(location)s, what_happened = %(what_happened)s, 
            sighting_date = %(sighting_date)s, number_of = %(number_of)s
            WHERE sightings.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# Delete function. Super simple. 

    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM sightings 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# This is the validator function. It is invoked on the routes with the post method. Flash is imported from
# flask. 

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['location']) < 1:
            flash("Location must be included!")
            is_valid = False
        if len(form_data['what_happened']) < 1:
            flash("What happened must be included!")
            is_valid = False
        if len(form_data['number_of']) < 1:
            flash("Must include number of Sasquatches!")
            is_valid = False
        elif int(form_data['number_of']) < 1:
            flash("Must see one Sasquatch!")
            is_valid = False
        if len(form_data['sighting_date']) < 1:
            flash("Sighting date required!")
            is_valid = False
        return is_valid