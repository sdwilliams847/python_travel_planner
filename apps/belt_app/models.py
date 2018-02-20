from __future__ import unicode_literals
from django.db import models
from datetime import date
import time
import bcrypt

class UserManager(models.Manager):
    def register(self, name, username, password, confirm_password):
        
        UserValidOrErrors = {
            "errors": [],
            "user": None,
            "valid": True
        }
        
        if len(name) < 3:
            UserValidOrErrors["valid"] = False
            UserValidOrErrors["errors"].append("First name is required")
        if len(username) < 3:
            UserValidOrErrors["valid"] = False
            UserValidOrErrors["errors"].append("First name is required")    
        else:
            username_list = User.objects.filter(username=username.lower())
            if len(username_list) > 0:
                UserValidOrErrors["valid"] = False
                UserValidOrErrors["errors"].append("Username already exists")
        if len(password) < 8:
            UserValidOrErrors["valid"] = False
            UserValidOrErrors["errors"].append("Password must be at least 8 characters")
        if confirm_password != password:
            UserValidOrErrors['valid'] = False
            UserValidOrErrors["errors"].append("Passwords do not match")
        
        if UserValidOrErrors['valid']:
            User.objects.create(
                name=name,
                username=username.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )
            UserValidOrErrors['user'] = User.objects.get(username=username.lower())
            
            print UserValidOrErrors['user'].name
            print "*****************"
            print UserValidOrErrors
        return UserValidOrErrors

    def login(self, username, password):
        response = {
            "errors": [],
            "user": None,
            "valid": True
        }
        
        if len(username) < 1:
            response["valid"] = False
            response["errors"].append("Username address is required")

        else:
            username_list = User.objects.filter(username=username.lower())
            if len(username_list) == 0:
                response["valid"] = False
                response["errors"].append("Username or password does not match.")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be at least 8 characters")
        if response["valid"]:
            if bcrypt.checkpw(password.encode(), username_list[0].password.encode()):
                response["user"] = username_list[0]
            else:
                response["valid"] = False
                response["errors"].append("Incorrect Password")
        return response

class TripManager(models.Manager):
    def add_trip(self, destination, plan, start_date, end_date, planner):

        response = {
            "errors": [],
            "trip": None,
            "valid": True
        }
        
        today = time.strftime("%Y-%m-%d")

        if len(destination) < 4:
            response["valid"] = False
            response["errors"].append("A destination is required for your trip")
        if len(plan) < 5:
            response["valid"] = False
            response["errors"].append("A plan is required for your trip") 
        if today > start_date:
            response["valid"] = False
            response["errors"].append("The departure date must be later than today")
        if start_date > end_date:
            response["valid"] = False
            response["errors"].append("Your return date must be after your departure date.")

        if response['valid']:
            response["trip"] = Trip.objects.create(
                destination=destination,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                planner=planner
            )
            # response['user'] = User.objects.get(id=planner_id.id)
            
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.CharField(max_length=1000)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    planner = models.ForeignKey(User, related_name="planned")

    objects = TripManager()

class Companion(models.Model):
    user = models.ForeignKey(User, related_name="joined_trips")
    trip = models.ForeignKey(Trip, related_name="joined_users")