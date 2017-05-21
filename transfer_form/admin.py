from django.contrib import admin

# Register your models here.
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'ssn', 'balance')


