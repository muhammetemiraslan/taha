from django.db import models
from ckeditor.fields import RichTextField

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