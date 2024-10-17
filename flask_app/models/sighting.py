from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from datetime import datetime

from flask_app.models import user



import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")




class Sighting:
    def __init__(self, data):
        self.id = data["id"]
        self.location = data["location"]
        self.date_of_sighting = data["date_of_sighting"]
        self.number_of_sasquatches = data["number_of_sasquatches"]
        self.what_happened = data["what_happened"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        # self.first_name = data["first_name"]


        self.blogger = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings LEFT JOIN users ON users.id = sightings.user_id"
        results = connectToMySQL("users_and_sightings").query_db(query)
        all_sightings = []
        print(all_sightings)
        for r in results:
            sighting = cls(r)
            sighting.blogger = user.User({
                "id": r["user_id"],
                "first_name": r["first_name"],
                "last_name": r["last_name"],
                "email": r["email"],
                "password": r["password"],
                "created_at": r["created_at"],
                "updated_at": r["updated_at"]
            })
            all_sightings.append(sighting)
        print("hi")
        return all_sightings
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location, date_of_sighting, number_of_sasquatches, what_happened, user_id) VALUES (%(location)s, %(date_of_sighting)s, %(number_of_sasquatches)s, %(what_happened)s, %(user_id)s);"
        print("here")
        return connectToMySQL("users_and_sightings").query_db(query, data)
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM sightings WHERE sightings.id = %(id)s;"
        data = {"id": id}
        results = connectToMySQL("users_and_sightings").query_db(query,data)
        print(results)
        return cls(results[0])
    

    @classmethod
    def update(cls,data):
        query = """
                sightings
            SET
                location = %(location)s,
                date_of_sighting = %(date_of_sighting)s,
                number_of_sasquatches = %(number_of_sasquatches)s,
                what_happened = %(what_happened)s
                
                
            WHERE
                sightings.id = %(id)s;
        """
        results = connectToMySQL("users_and_sightings").query_db(query,data)
        # print(results)
        return results
    
    @classmethod
    def delete(cls,id):
        query  = "DELETE FROM sightings WHERE sightings.id = %(id)s;"
        data = {"id": id}
        return connectToMySQL("users_and_sightings").query_db(query, data)
    

    
    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting["location"]) < 3:
            flash("Location is required and must atleast be 3 characters")
            is_valid = False
        
        if len(sighting["what_happened"]) < 3:
            flash(" Minimum text here is atleast 3 characters")
            is_valid = False

        if int(sighting["number_of_sasquatches"]) < 1:
            flash("Please enter a valid number of Sasquatches")
            is_valid = False
        
        c_time = datetime.now()
        current_date = c_time.strftime("%Y-%m-%d")
        print("current time is", current_date)
        print("time to compare is", sighting["date_of_sighting"])
        if (sighting["date_of_sighting"]) >= current_date:
            flash("Date must be in the past", "error")
            is_valid = False
        # Check if date_of_sighting is in the past
        # if date_of_sighting >= datetime.now():
        #     flash("Date of sighting must be in the past")
        #     is_valid = False
        # date_of_sighting = datetime.strptime(date_of_sighting, '%Y-%m-%d')
        # print (sighting["date_of_sighting"])
        # if date_of_sighting != datetime.now():   
        #     flash("Date of sighting must be in the past")
        #     is_valid = False
        # date_pattern = datetime.strptime(date_pattern, '%m/%d/%Y')
        # if not re.match(r'\d{2}/\d{2}/\d{4}', sighting["date_of_sighting"]):
        #     flash("Invalid date format")
        #     is_valid = False
        # else: 
        #     date_of_sighting = datetime.strptime(sighting["date_of_sighting"], '%m/%d/%Y')
        #     if date_of_sighting > datetime.now():   
        #         flash("Date of sighting must be in the past")
        #         is_valid = False
        return is_valid

      


        
        # date_string = recipe.get("date_made")
        # date_format = "%%m/%%d/%%Y"
        # if date_string:
        #     if not re.match(date_format, date_string):
        #         flash("Date is required")
        #         is_valid = False
        # if "under" not in recipe:
        #     flash("Does your recipe take less than 30 min?")
        #     is_valid = False
        # return is_valid