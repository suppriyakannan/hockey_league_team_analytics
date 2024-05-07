from django.contrib import admin
from .models import Team

admin.site.register(Team)
from .models import Goal

admin.site.register(Goal)
