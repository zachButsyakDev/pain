
from django.contrib import admin
from django.urls import path, include
# all of these contain their own sub paths from other directories and folders (i.e. here we define path(calendar/ include(calendar_page.urls)) which essentially initializes the calendar/ path by itself and then pulls other paths from the .urls file listed in include arguments. For example, we could go to calendar/view_calendar/ should it be defined within calendar_pages.urls (which it isnt)). 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # core app has home and login page
    path('notes/', include('note_page.urls')),
    path('calendar/', include('calendar_page.urls')),
    path('users/', include('users.urls')),
]
