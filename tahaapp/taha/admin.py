from django.contrib import admin
from .models import News
from ckeditor.widgets import CKEditorWidget
from django.db import models

class NewsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget()},
    }
    list_display = ("title", "category", "date_published")
    list_filter = ("category","date_published")

admin.site.register(News, NewsAdmin)
