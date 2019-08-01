import datetime
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.db import models
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils.text import slugify


class S7User(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    def num_uploads(self):
        return Upload.objects.filter(user=self).count()

    def num_reviews(self):
        return Review.objects.filter(user=self).count()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user(sender, instance, created, **kwargs):
    if created:
        S7User.objects.create(user=instance)


class Upload(models.Model):
    url = models.CharField(max_length = 100)
    user = models.ForeignKey(S7User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    description = models.TextField(verbose_name="Upload Description")
    versionNotes = models.TextField(verbose_name="Version Notes")
    uploadDate = models.DateTimeField('date published')
    versionNumber = models.DecimalField(max_digits=5, decimal_places = 1)
    total_downloads = models.IntegerField()
    version_downloads = models.IntegerField()


    def indexScreenshot(self):
        return Screenshot.objects.filter(upload=self)[0].url


    def avg_review(self):
        reviews = Review.objects.filter(upload=self)
        num_reviews = reviews.count()
        if num_reviews == 0:
            return 0
        else:
            return reviews.aggregate(Sum('rating'))['rating__sum'] / reviews.count()


    def total_stars(self):
        reviews = Review.objects.filter(upload=self)
        num_reviews = reviews.count()
        if num_reviews == 0:
            return 0
        else:
            return reviews.aggregate(Sum('rating'))['rating__sum']


    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    uploads = models.ManyToManyField(Upload, related_name='tags')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        print("slug: ", self.slug)
        super(Tag, self).save(*args, **kwargs)


class Screenshot(models.Model):
    url = models.CharField(max_length = 100)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Review(models.Model):
    title = models.CharField(max_length = 50)
    text = models.TextField(max_length = 2048, verbose_name="Review Text")
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    user = models.ForeignKey(S7User, on_delete=models.CASCADE)
    pubDate = models.DateTimeField('date published')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.user.user.username + self.upload.title

