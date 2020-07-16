from django.db import models

# Create your models here.

class Blogpost(models.Model):
    blog_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_date = models.CharField(max_length=50)
    brief = models.CharField(max_length=200)
    intro1 = models.CharField(max_length=2000)
    intro2 = models.CharField(max_length=2000)
    subheading1 = models.CharField(max_length=200)
    content1 = models.CharField(max_length=2000)
    subheading2 = models.CharField(max_length=200)
    content2 = models.CharField(max_length=2000)
    subheading3 = models.CharField(max_length=200)
    content3 = models.CharField(max_length=2000)
    about_content = models.CharField(max_length=500)
    image = models.ImageField(upload_to='blog/images', default='')

    def __str__(self):
        return self.post_title
