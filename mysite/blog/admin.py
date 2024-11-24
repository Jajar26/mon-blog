from django.contrib import admin
from .models import Equipment, Athlete

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'reserved_by', 'reservation_datetime', 'image_thumbnail')
    list_filter = ('category', 'status')
    search_fields = ('name',)
    fields = ('name', 'category', 'status', 'reserved_by', 'reservation_datetime', 'image')

    def image_thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'  
        return 'No Image'
    image_thumbnail.allow_tags = True 

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('name', 'objective', 'is_using_machine', 'created_at')
    list_filter = ('is_using_machine',)  
    search_fields = ('name', 'objective')
    
