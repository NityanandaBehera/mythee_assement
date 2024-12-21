from django.urls import path
from .views import (
    SignupView,
    SigninView,
    LogoutView,
    ProfileView,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
)

urlpatterns = [
    # Authentication Endpoints
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/signin/', SigninView.as_view(), name='signin'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # Blog Post Endpoints
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Comment Endpoints
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
