from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Project)
admin.site.register(models.Milestone)
admin.site.register(models.Update)
admin.site.register(models.Customer)
admin.site.register(models.ChecklistItem)