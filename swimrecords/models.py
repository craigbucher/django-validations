from django.db import models
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as text
from django.core.validators import *
from django.utils import timezone
from django import forms

def validate_first_name(first_name):
	if len(first_name) == 0:
		raise ValidationError(text("First name field can not be blank!"))

def validate_last_name(last_name):
	if len(last_name) == 0:
		raise ValidationError(text("Last name field can not be blank!"))

def validate_team_name(team_name):
	if len(team_name) == 0:
		raise ValidationError(text("Team name field can not be blank!"))

def validate_relay(relay):
	if relay not in ['True', 'False']:
		raise ValidationError(text("Relay value must be either 'True' or 'False'!"))

def validate_stroke(stroke):
    strokes = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if stroke not in strokes:
        raise ValidationError(text(f"Acceptable values are: {strokes}"))

def validate_record_date(record_date):
    if record_date > timezone.now():
            raise ValidationError(text("The date cannot be in the future!"))

class SwimRecord(models.Model):
    #pass # delete me when you start writing in validations
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    relay = models.BooleanField()
    stroke = models.CharField(max_length=13, validators=[validate_stroke])
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators=[validate_record_date], blank='true')
    record_broken_date = models.DateTimeField()

# from: https://docs.djangoproject.com/en/4.0/ref/forms/validation/
# 'Cleaning and validating fields that depend on each other'
# from django import forms
# previous error: 'zero-argument form of "super" call is valid only within a class
# so, moved here from above
    def clean(self):
        cleaned_data = super().clean()
        if self.record_date and self.record_broken_date:
            if self.record_date > self.record_broken_date:
                    raise ValidationError({'record_broken_date':"Can't break record before record was set."})
