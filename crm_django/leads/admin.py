from django.contrib import admin
from .models import (
    Lead, 
    Agent, 
    User, 
    UserProfile, 
    Category
)

admin.site.register([Lead, User, Agent, UserProfile, Category])
