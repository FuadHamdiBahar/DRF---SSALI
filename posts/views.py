from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import (
    IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
)
from rest_framework.pagination import PageNumberPagination
from accounts.serializers import CurrentUserPostSerializer
from drf_yasg.utils import swagger_auto_schema

from .models import Post
from .serializers import PostSerializer
from .permissions import ReadOnly, AuthorOrReadOnly

class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"

@api_view(http_method_names=['GET', 'POST'])
@permission_classes([AllowAny])
def homepage(request:Request):
    
    if request.method == 'POST':
        data = request.data
        
        response = {'message': 'Hello World', 'data':data}
        
        return Response(data=response, status=status.HTTP_201_CREATED)
    
    response = {'message': 'Hello World'}
    return Response(data=response, status=status.HTTP_200_OK)

# MIXINS
class PostListCreateView(generics.GenericAPIView, mixins.ListModelMixin,
    mixins.CreateModelMixin):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().order_by('id')
    pagination_class = CustomPaginator
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)
    
    @swagger_auto_schema(
        operation_summary='List all posts',
        operation_description='This returns a list of all posts'
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a post',
        operation_description='Creates a post'
    )
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PostRetrieveUpdateDeleteView(generics.GenericAPIView, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]
    queryset = Post.objects.all()
    
    @swagger_auto_schema(
        operation_summary='Retrieve a post by id',
        operation_description='This retrieves a post by an id'
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a post by id',
        operation_description='This updates a post given the id'
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a post',
        operation_description='This deletes a post given the id'
    )
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request:Request):
    user = request.user

    serializer = CurrentUserPostSerializer(instance=user, context = {'request':request})
    
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # username = self.kwargs.get('username') ini kalau urlsnya ada parameter
        # sedangkan yang dibawah ada params jg tapi tidak wajib
        # contoh .../posts_for/?username=fuad return yang usernamenya fuad
        # contoh .../posts_for return all
        # harus berhati hati pada bagian definisi urlnsya
        username = self.request.query_params.get('username') or None
        
        queryset = Post.objects.all()
        
        if username is not None:
            return Post.objects.filter(author__username=username)

        return queryset
    
    @swagger_auto_schema(
        operation_summary='List posts for an author (user)',
        operation_description='This updates a post given the id'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
# CLASS BASED VIEW

# class PostListCreateView(APIView):
#     serializer_class = PostSerializer
    
#     """
#         a view for creating and listing posts
#     """
    
#     def get(self, request: Request, *args, **kwargs):
#         posts = Post.objects.all()
        
#         serializer = self.serializer_class(instance=posts, many=True)
        
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request: Request, *args, **kwargs):
#         data = request.data
        
#         serializer = self.serializer_class(data=data)
        
#         if serializer.is_valid():
#             print(serializer)
#             serializer.save()
#             response = {
#                 'message': 'Post Created',
#                 'data': serializer.data
#             }
#             return Response(data=response, status=status.HTTP_201_CREATED)
        
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostRetrieveUpdateDeleteView(APIView):
#     serializer_class = PostSerializer
    
#     def get(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)
        
#         serializer = self.serializer_class(instance=post)
        
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request: Request, post_id:int):
#         post = get_object_or_404(Post, pk=post_id)
        
#         data = request.data
        
#         serializer = self.serializer_class(instance=post, data=data)

#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 'message': 'Post Updated',
#                 'data': serializer.data
#             }       
#             return Response(data=response, status=status.HTTP_200_OK)

#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request: Request, post_id:int):
#         post = get_object_or_404(Post, pk=post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# FUNCTION BASE VIEW

# @api_view(http_method_names=['GET', 'POST'])
# def list_posts(request:Request):
    # posts = Post.objects.all()
    
    # if request.method == 'POST':
    #     data = request.data
    #     serializer = PostSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Post Created',
    #             'data': serializer.data
    #         }
    #         return Response(data=response, status=status.HTTP_201_CREATED)
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # serializer = PostSerializer(instance=posts, many=True)
    
    # response = {
    #     'message': 'post',
    #     'data': serializer.data
    # }
    
    # return Response(data=response, status=status.HTTP_200_OK)

# @api_view(http_method_names=['GET'])
# def post_detail(request:Request, post_id:int):
#     post = get_object_or_404(Post, pk=post_id)
    
#     serializer = PostSerializer(instance=post)
    
#     response = {
#         'message': 'post',
#         'data': serializer.data
#     }
#     return Response(data=response, status=status.HTTP_200_OK)

# @api_view(http_method_names=['PUT'])
# def update_post(request: Request, post_id: int):
#     post = get_object_or_404(Post, pk=post_id)
    
#     data = request.data
    
#     serializer = PostSerializer(instance=post, data=data)

#     if serializer.is_valid():
#         serializer.save()
        
#         response = {
#             'message': 'Post Updated Successfully',
#             'data': serializer.data
#         }
        
#         return Response(data=response, status=status.HTTP_200_OK)
    
#     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(http_method_names=['DELETE'])
# def delete_post(request: Request, post_id: int):
#     post = get_object_or_404(Post, pk=post_id)
    
#     post.delete()
    
#     return Response(status=status.HTTP_204_NO_CONTENT)