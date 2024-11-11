from django.contrib import admin
from .models import Alert

class AlertsAdmin(admin.ModelAdmin):
    search_fields = ['profile__email']  # Adds search functionality for profile email

admin.site.register(Alert, AlertsAdmin)