from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog import views


urlpatterns = [
    path('equipment', views.equipment_list, name='equipment_list'), 
    path('', views.home, name='home'), 
    path('athletes/', views.athlete_list, name='athlete_list'),
    path('add-athlete/', views.add_athlete, name='add_athlete'),
    path('equipment/update_status/<int:equipment_id>/', views.update_equipment_status, name='update_equipment_status'),
    path('delete/<str:athlete_name>/', views.delete_athlete, name='delete_athlete'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)