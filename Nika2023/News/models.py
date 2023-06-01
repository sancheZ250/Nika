from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    is_published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('news_details', kwargs={'pk': self.id})

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')


class NewsImage(models.Model):
    id = models.AutoField(primary_key=True)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_images/')
