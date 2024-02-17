from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, permissions
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthorOrReadOnly

from blog.models import Post
from .serializers import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['body', 'author__username']
    # ordering_fields = ['author_id', 'publish']
    ordering_fields = '__all__'
    ordering = ['body']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (permissions.IsAdminUser,)


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)


# Create your views here.
