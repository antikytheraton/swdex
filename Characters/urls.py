from django.conf.urls import url
from .views import index

urlpatterns = [
    url(r'^$', index),
    url(r'^(?P<pagina>[0-9]+)/$',index)
]
