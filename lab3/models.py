from __future__ import unicode_literals

from django.db import models

# Create your models here.
class planes(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)

    def __str__(self):
        return  self.model


class departure(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)

    def __str__(self):
        return self.city

class destination(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)

    def __str__(self):
        return self.city


class airlines(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return  self.name

class flights(models.Model):
    id = models.IntegerField(primary_key=True)
    airlines_id = models.ForeignKey(airlines, related_name='airline')
    departure_id = models.ForeignKey(departure, related_name='departure')
    destination_id = models.ForeignKey(destination, related_name='destination')
    plane_id = models.ForeignKey(planes, related_name='plane')
    departure_time = models.CharField(max_length=1000)

