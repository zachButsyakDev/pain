from django.contrib import admin
from .models import NoteSection, Note

@admin.register(NoteSection)
class NoteSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'section', 'updated_at')
    list_filter = ('user', 'section')
    search_fields = ('title', 'content')
