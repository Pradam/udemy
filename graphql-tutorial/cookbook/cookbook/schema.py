import graphene

import ingredients.schema


class Mutation(ingredients.schema.Mutation, graphene.ObjectType):
    pass


class Query(ingredients.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,
                         mutation=Mutation)