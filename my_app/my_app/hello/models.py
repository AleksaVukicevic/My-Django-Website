from django.db import models

class FridgeItem(models.Model):
	text = models.TextField()

class UserData(models.Model):
	user_id = models.IntegerField()
	fridge_items = []
