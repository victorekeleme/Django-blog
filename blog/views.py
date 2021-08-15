from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from blog.models import Post, Category
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog.forms import SignUpForm, PostForm

from rest_framework import viewsets
from .serializers import CategorySerializer
# Create your views here.



class CategoryMixin(object):
    def get_categories(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        return context




class PostListView(CategoryMixin, ListView):
    context_object_name = 'posts'
    model = Post
    paginate_by = 8
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        posts = Post.objects.all()
        #context['featured_post'] = posts[0]
        return context

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class CategoryDetailView(CategoryMixin,DetailView):
    context_object_name = 'category'
    model = Category
    template_name = 'blog/category_detail.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context =super(CategoryDetailView, self).get_context_data(**kwargs)
        cat_posts = self.get_cat_posts()
        context['cat_posts'] = cat_posts
        context['page_obj'] = cat_posts
        return context

    def get_cat_posts(self):
        queryset = self.get_categories()
        paginator = Paginator(queryset,8)
        page = self.request.GET.get('page')
        cat_posts = paginator.get_page(page)
        return cat_posts


class SearchPostView(CategoryMixin, ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'blog/search_post_list.html'

    def get_context_data(self, **kwargs):
        context = super(SearchPostView, self).get_context_data(**kwargs)
        s_posts = self.get_posts()
        context['s_posts'] = s_posts
        context['page_obj'] = s_posts
        return context

    def get_posts(self):
        search = self.request.GET.get('q')
        if search != '' and search is not None:
            searched = Post.objects.filter(title__icontains=search)
        queryset = searched
        paginator = Paginator(queryset, 8)
        page = self.request.GET.get('page')
        s_posts = paginator.get_page(page)
        return s_posts


class PostDetailView(CategoryMixin, DetailView):
    context_object_name = 'post'
    model = Post


class DashBoardView(CategoryMixin, ListView):
    template_name = 'dashboard/dpost_list.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        d_posts = self.get_dposts()
        context['d_posts'] = d_posts
        context['page_obj'] = d_posts
        return context


    def get_dposts(self):
        queryset = Post.objects.filter(author_id=self.request.user)
        paginator = Paginator(queryset, 8)
        page = self.request.GET.get('page')
        d_posts = paginator.get_page(page)
        return d_posts


class DraftPostView(ListView):
    context_object_name = "drafts"
    template_name = 'dashboard/draft_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date=None)


class PostCreateView(CreateView):
    template_name = 'dashboard/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_drafts')

    def form_valid(self, form):
        post_form = form.save(commit=False)
        post_form.author = self.request.user
        post_form.save()
        return super(PostCreateView, self).form_valid(form)

        
class DashboardSearchView(CategoryMixin, ListView):
    model = Post
    template_name = 'dashboard/dsearch_list.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardSearchView, self).get_context_data(**kwargs)
        s_posts = self.get_sposts()
        context['s_posts'] = s_posts
        context['page_obj'] = s_posts
        return context

    def get_sposts(self):
        search = self.request.GET.get('q')
        if search != '' and search is not None:
            searched = Post.objects.filter(author_id=self.request.user, title__icontains=search)
        queryset = searched
        paginator = Paginator(queryset, 8)
        page = self.request.GET.get('page')
        s_posts = paginator.get_page(page)
        return s_posts


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'dashboard/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'dashboard/post_form.html'

    success_url = reverse_lazy('dashboard')

def Like_Post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    return HttpResponseRedirect('post_list')

def publish_post(request,slug):
    post = get_object_or_404(Post, slug=slug)
    post_slug = post.slug
    post.publish()
    return redirect('dashboard')





#REST API
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer






