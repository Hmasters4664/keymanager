from django.conf.urls import url
from django.urls import include, re_path, path
from mnager import views
from .views import PutKey, ListKeys, UpdateKey


urlpatterns = [
    path('register', views.create_user, name='register'),
    path('newkey', PutKey.as_view(), name='new'),
    path('list', ListKeys.as_view(), name='list'),
    path('update/<slug:slug>', UpdateKey.as_view(), name='update'),
]