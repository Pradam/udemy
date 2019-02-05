from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name="ingredents",
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=100)
    genus = models.CharField(max_length=100)
    is_domesticated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
