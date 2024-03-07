from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-news', args=[f"{self.slug}"])


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)


class News(models.Model):

    class Status(models.TextChoices):
        Draft = "DF", "Draft"
        Published = "PB", "Published"

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images/', null=True)
    show_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    publish_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.Draft
    )

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', args=[f'{self.slug}'])


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.author} - {self.news}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.author} - {self.comment}"


class CountView(models.Model):
    count = models.GenericIPAddressField()
