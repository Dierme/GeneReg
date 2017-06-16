from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
rgx_validator = RegexValidator("^[a-zA-Z]+$", "Name should consist only from Latin letters.")


class Names(models.Model):
    name = models.CharField(max_length=255, unique=True, validators=[rgx_validator])
    pub_date = models.DateTimeField('date added')
