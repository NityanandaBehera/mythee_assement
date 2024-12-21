from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
)
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from rest_framework.pagination import PageNumberPagination

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                login(request, user)
                csrf_token = get_token(request)
                return Response(
                    {"message": "Login successful.","csrf_token": csrf_token},
                    status=status.HTTP_200_OK
                )
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Post Views
class PostListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Filter based on the author's username (optional)
        author = request.GET.get('author', None)
        posts = Post.objects.all().order_by('-created_at')
        
        if author:
            posts = posts.filter(author__username__icontains=author)
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set number of posts per page
        page = paginator.paginate_queryset(posts, request)

        # Serialize the posts
        serializer = PostSerializer(page, many=True)
        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise PermissionDenied({"error": "Post not found."})

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            raise PermissionDenied({"error": "You are not authorized to edit this post."})

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            raise PermissionDenied({"error": "You are not authorized to delete this post."})

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Comment Views
class CommentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id, parent=None).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        data = request.data
        data['post'] = post_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        """Retrieve a comment object or raise a 404 error."""
        return get_object_or_404(Comment, pk=pk)

    def get(self, request, pk):
        """Retrieve a single comment by its ID."""
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        comment = self.get_object(pk)
    
    # Check if the logged-in user is the author of the comment
        if comment.author != request.user:
            raise PermissionDenied({"error": "You are not authorized to delete this comment."})
    
    # Delete the comment
        comment.delete()

    # Return a response confirming deletion
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
