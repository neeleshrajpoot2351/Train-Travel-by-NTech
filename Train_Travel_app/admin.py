from django.contrib import admin
from django.contrib.admin.sites import site
from .models import User
from .models import Train, Station, TrainStation

from .models import TrainStation
class TrainStationAdmin(admin.ModelAdmin):
    list_display = ('train', 'station', 'stop_number', 'platform_number')


class UserAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'email', 'password')

admin.site.register(User,UserAdmin)




class TrainStationInline(admin.TabularInline):
    model = TrainStation
    extra = 1  # Number of blank forms shown by default

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_number', 'train_name', 'origin', 'destination')
    search_fields = ('train_number', 'train_name', 'origin__name', 'destination__name')
    inlines = [TrainStationInline]  # Allows you to add stations to a train in admin


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

