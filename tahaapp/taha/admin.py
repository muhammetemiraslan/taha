from django.contrib import admin
from .models import News, AboutContent, Category
from ckeditor.widgets import CKEditorWidget
from django.db import models


class NewsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget()},
    }
    list_display = ("title", "category", "date_published")
    list_filter = ("category", "date_published")


admin.site.register(News, NewsAdmin)


class AboutContentAdmin(admin.ModelAdmin):
    list_display = ("title","category","image","slug")
    list_filter = ("category",)
    readonly_fields = ("slug",)


admin.site.register(Category)
admin.site.register(AboutContent, AboutContentAdmin)
