from django.db import models

# Create your models here.

class Urls_DB(models.Model):
	url = models.CharField(max_length=300)
    
	def __str__(self):
		return self.url
