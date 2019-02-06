import django_filters

import graphene

from graphene_django.types import DjangoObjectType

from graphene_django.filter import DjangoFilterConnectionField

from .models import (Category, Ingredient, Animal, Post)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name']
        interfaces = (graphene.relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
                        'name': ['exact', 'icontains', 'istartswith'],
                        'notes': ['exact', 'icontains'],
                        'category': ['exact'],
                        'category__name': ['exact']}
        interfaces = (graphene.relay.Node, )


class AnimalNode(DjangoObjectType):
    class Meta:
        model = Animal
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'genus': ['exact'],
            'is_domesticated': ['exact'],
        }
        interfaces = (graphene.relay.Node, )


class AnimalFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Animal
        fields = ['id', 'name', 'genus', 'is_domesticated']

    @property
    def qs(self):
        return super(AnimalFilter, self).qs.all()


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        only_fields = ['title', 'content']
        filter_fields = ['content']
        interfaces = (graphene.relay.Node,)


class CreatePost(graphene.Mutation):
    title = graphene.String()
    content = graphene.String()

    class Arguments:
        title = graphene.String()
        content = graphene.String()
        owner_id = graphene.Int()

    def mutate(self, info, **kwargs):
        post = Post(**kwargs)
        post.save()

        return CreatePost(title=post.title,
                          content=post.content)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()


class Query(object):
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    all_categories = graphene.List(CategoryType)
    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())
    all_ingredients = graphene.List(IngredientType)
    node_category = graphene.relay.Node.Field(CategoryNode)
    node_all_category = DjangoFilterConnectionField(CategoryNode)
    node_ingredient = graphene.relay.Node.Field(IngredientNode)
    node_all_ingredient = DjangoFilterConnectionField(IngredientNode)
    animal = graphene.relay.Node.Field(AnimalNode, filterset_class=AnimalFilter)
    all_animal = DjangoFilterConnectionField(AnimalNode, filterset_class=AnimalFilter)
    post = graphene.relay.Node.Field(PostNode)
    all_post = DjangoFilterConnectionField(PostNode)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.select_related('category').all()

    def resolve_category(self, info, **kwargs):
        _id = kwargs.get('id')
        name = kwargs.get('name')

        if _id is not None:
            return Category.objects.get(pk=_id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        _id = kwargs.get('id')
        name = kwargs.get('name')

        if _id is not None:
            return Ingredient.objects.get(pk=_id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None