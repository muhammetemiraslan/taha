from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.

class News(models.Model):
    CATEGORY_CHOICES = [
        ('politics', 'Politika'),
        ('sports', 'Spor'),
        ('economy', 'Ekonomi'),
        ('Business', 'İş Dünyası'),
        ('Technology', 'Teknoloji'),
        ('Science', 'Science'),
        ('Health', 'Sağlık'),
        # Diğer kategoriler eklenebilir
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='politics')
    description = RichTextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)  # Fotoğraf dosyasının yeri
    date_published = models.DateField()
    
    def __str__(self):
        return self.title
    
    
class AboutContent(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='about_images/')
    description = RichTextField()
    category = models.ForeignKey('Category', related_name="contents", on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)