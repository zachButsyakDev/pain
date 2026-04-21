from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes'),
    path('create/', views.create_note, name='create_note'),
    path('view/<int:id>/', views.note_view, name='note_view'),
    path('edit/<int:id>/', views.edit_note, name='edit_note'),
    path('delete/<int:id>/', views.delete_note, name='delete_note'),
    # Sections
    path('section/create/', views.create_note_section, name='create_note_section'),
    path('section/edit/<int:id>/', views.update_note_section, name='update_note_section'),
    path('section/delete/<int:id>/', views.delete_note_section, name='delete_note_section'),
]
