from django.urls import path

from . import views

urlpatterns = [
    path('homepage/', views.homepage, name='posts_home'),
    # mixins
    path('', views.PostListCreateView.as_view(), name='list_posts'),
    path('<int:pk>/', views.PostRetrieveUpdateDeleteView.as_view(), name='post_detail'),
    # class based view
    # path('', views.PostListCreateView.as_view(), name='list_posts'),
    # path('<int:post_id>/', views.PostRetrieveUpdateDeleteView.as_view(), name='rud_posts')
    # function base view
    # path('', views.list_posts, name='list_posts'),
    # path('<int:post_id>', views.post_detail, name='post_detail'),
    # path('update/<int:post_id>/', views.update_post, name='update_post'),
    # path('delete/<int:post_id>', views.delete_post, name='delete_post')
    path('current_user/', views.get_posts_for_current_user, name='current_user'),
    # path('posts_for_current_user/', views.ListPostsForAuthor.as_view(), name='posts_for_current_user'),
    path('posts_for/', views.ListPostsForAuthor.as_view(), name='posts_for_current_user'),
]
