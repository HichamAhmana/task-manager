from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql_jwt.middleware import JSONWebTokenMiddleware

from config.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
                graphiql=True,
                middleware=[JSONWebTokenMiddleware()]
            )
        ),
    ),
]
