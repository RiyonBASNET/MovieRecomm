from django.contrib import admin

from .models import Review, UserProfile

# Register your models
admin.site.register(Review)
admin.site.register(UserProfile)
# admin.site.register(Favorite)
