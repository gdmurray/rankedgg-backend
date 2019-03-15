from django.contrib import admin
from .models import Operator


# Register your models here.
class OperatorAdmin(admin.ModelAdmin):
    fields = ('name', 'type', 'logo', 'image')
    list_display = ('name', 'type')


admin.site.register(Operator, OperatorAdmin)
