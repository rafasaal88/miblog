from django.contrib import admin
from principal.models import Entry
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField
from . import models

class EntryAdmin(MarkdownModelAdmin):
          list_display = ("title", "created")
          
          # Next line is a workaround for Python 2.x
          formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}


admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Comentario)
admin.site.register(models.Mensaje)