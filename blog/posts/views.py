import time
from django.http import HttpRequest
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify

from django.forms import ModelForm, model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework import permissions

from .serializers import PostSerializer

from .models import Post
from .forms import CommentForm, PostForm
from .permissions import IsOwnerOrReadOnly


class PostsHome(ListView):
    paginate_by = 5
    model = Post
    context_object_name = "posts"
    template_name = "posts/home.html"

    def get_queryset(self):
        return Post.objects.all()


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = "posts/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"
    form_class = CommentForm

    def get_success_url(self) -> str:
        return reverse("post_detail", kwargs={"post_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = context["post"].comments.all()
        print(context["comments"])
        context["form"] = CommentForm()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login", permanent=True)

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form, request.user.username)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: ModelForm, username):
        comment = form.save(commit=False)
        comment.name = username
        comment.post = self.object
        comment.save()
        return super(PostDetail, self).form_valid(comment)


class PostCreationView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "posts/post_create_form.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.slug = slugify(self.request.POST["title"])
        post.author = self.request.user
        post.save()
        return super(PostCreationView, self).form_valid(form)


# class PostAPIView(APIView):
#     def get(self, request):
#         lst = Post.objects.all()
#         return Response({'posts': PostSerializer(lst, many=True).data})

#     def post(self, request: Request):
#         print(type(request.user))

#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'message': serializer.data})

#     def patch(self, requser, *args, **kwargs):
#         return Response({"message": "PATCH request"})


# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class PostCreateApiView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)


def handle_page_not_found(request, *args, **argv):
    return render(request, "posts/404.html", context={})
