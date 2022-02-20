from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('/category/<str:slug>/', views.category_page),
    path('/category/<str:slug>', views.category_page),
    path('/<int:pk>',views.PostDetail.as_view()),
    path('/<int:pk>/',views.PostDetail.as_view()),
    #path('',views.index),
    path('',views.PostList.as_view())
]

