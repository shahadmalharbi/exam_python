from django.db import models
import re
class UserManager(models.Manager):
    def basic_validator(self, postData,user = None):
        errors = {}
        if len(postData['name']) < 3:  #check if name greater than 3 characters
            errors['name'] = "Name cannot be shorter than 3 characters" 
        if len(postData['username']) < 3:#check if username greater than 3 characters
            errors['username'] = "Username cannot be shorter than 3 characters"
        if (User.objects.filter(username=postData['username']).exists()):
            errors['user_exists'] = "A user with that username already exists"
        elif len(postData['password']) < 8: #check if password greater than 8 characters.
            errors['password'] = "Password should be at least 8 characters"
        elif postData['password'] != postData['confirm_pw']: #check if confirm password match with password or not.
                errors['password'] = "Passwords DO NOT match!"
        elif len(postData['date_hired']) == 0:
                errors['date_hired'] = "Please enter a date"
        return errors
        
    def add_validator(self, postData):
        errors = {}
        if len(postData['item']) == 0:
            errors['item'] = "It's Empty, please enter an item"
        elif len(postData['item']) < 3:
            errors['item'] = "Item name should be greater than 3 characters"   
        return errors       

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    # Many to Many relationship:
    items = models.ManyToManyField('Item',related_name="users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Item(models.Model):
    item = models.CharField(max_length=255)
    # Many to one relationship: each user can add one ore many items(Wishs)
    added_by = models.ForeignKey(User,related_name="items_create", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
