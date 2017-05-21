import moneyed
from djmoney.models.fields import MoneyField

from django.db import models
from django.contrib.auth.models import User


class UserFullName(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()


class Person(models.Model):
    user = models.OneToOneField(UserFullName, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=14)
    balance = MoneyField(max_digits=10,
                         decimal_places=2, default_currency='RUB')

    def __str__(self):
        return "{0} {1}".format(self.user.first_name,
                                self.user.last_name)
