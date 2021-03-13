"""
Config admin panel
"""

from django.contrib import admin
from app.models import Photo, PhotoOpening, Setting, PhotoComment


admin.site.register((Photo, PhotoComment, PhotoOpening, Setting))
