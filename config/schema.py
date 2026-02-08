# config/schema.py
import graphene
from tasks.GraphQL.mutations import TaskMutation, UserMutation
from tasks.GraphQL.auth import AuthMutation
from tasks.GraphQL.queries import TaskQuery


class Query(TaskQuery, graphene.ObjectType):
    pass

class Mutation(TaskMutation, UserMutation, AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    
)
