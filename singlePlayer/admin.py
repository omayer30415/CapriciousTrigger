from django.contrib import admin
from .models import *
# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(User)
admin.site.register(Soldier)
admin.site.register(General)
admin.site.register(Team)
admin.site.register(Opponent)
admin.site.register(Score)
admin.site.register(Product)
