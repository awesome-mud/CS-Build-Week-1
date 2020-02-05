from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from util.generate_world import generate_rooms
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]


generate_rooms(10, 10, 100)
# bring a fucntion that genrates the rooms