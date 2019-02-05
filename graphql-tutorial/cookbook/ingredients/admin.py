from django.contrib import admin
from .models import Category, Ingredient, Animal, Post

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Animal)
admin.site.register(Post)
