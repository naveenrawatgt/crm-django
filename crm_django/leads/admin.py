from django.contrib import admin
from .models import Lead, Agent, User, UserProfile

admin.site.register([Lead, User, Agent, UserProfile])
