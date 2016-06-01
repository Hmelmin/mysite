# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Lab3Airlines(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'lab3_airlines'


class Lab3Departure(models.Model):
    city = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'lab3_departure'


class Lab3Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'lab3_destination'


class Lab3Flights(models.Model):
    id = models.IntegerField(primary_key=True)
    departure_time = models.CharField(max_length=1000)
    airlines_id = models.ForeignKey(Lab3Airlines, models.DO_NOTHING)
    departure_id = models.ForeignKey(Lab3Departure, models.DO_NOTHING)
    destination_id = models.ForeignKey(Lab3Departure, models.DO_NOTHING)
    plane_id = models.ForeignKey('Lab3Planes', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lab3_flights'


class Lab3Planes(models.Model):
    model = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'lab3_planes'
