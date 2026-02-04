import graphene
from tasks.GraphQL.queries import TaskQuery
from tasks.GraphQL.mutations import TaskMutation
from tasks.GraphQL.auth import AuthMutation

class Query(TaskQuery, graphene.ObjectType):
    pass

class Mutation(TaskMutation,AuthMutation ,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

