from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]

