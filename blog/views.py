from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, FormView ,CreateView, DeleteView, UpdateView
from blog.models import Post, Category, Comments
from profiles.models import Profile

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog.forms import SignUpForm, PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# REST API IMPORT
from rest_framework import viewsets
from .serializers import CategorySerializer, PostSerializer
# Create your views here.


# Category mixins to show category in all pages
class CategoryMixin(object):
    def get_categories(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        return context

# displays all posts
class PostListView(CategoryMixin, ListView):
    context_object_name = 'posts'
    model = Post
    paginate_by = 8
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['post_form'] = PostForm
        return context
    #
    # def get_queryset(self):
    #     return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


# creating post
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'profiles:login'
    template_name = 'blog/base.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')


    def form_valid(self, form):
        post_form = form.save(commit=False)
        post_form.author = self.request.user.profile
        post_form.save()
        return super(PostCreateView, self).form_valid(form)

# displays posts by category
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
        context['post_form'] = PostForm
        return context

    def get_cat_posts(self):
        queryset = self.get_categories()
        paginator = Paginator(queryset,8)
        page = self.request.GET.get('page')
        cat_posts = paginator.get_page(page)
        return cat_posts


# search for post
class SearchPostView(CategoryMixin, ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'blog/search_post_list.html'

    def get_context_data(self, **kwargs):
        context = super(SearchPostView, self).get_context_data(**kwargs)
        s_posts = self.get_posts()
        context['post_form'] = PostForm
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


# displays post detail
class PostDetailView(CategoryMixin, DetailView):
    context_object_name = 'post'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.all()
        context['form'] = CommentForm
        context['post_form'] = PostForm

        return context

    # create comment in post detailview
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        comment_form = form.save(commit=False)
        if form.is_valid():
            post = self.get_object()
            comment_form.author = self.request.user.profile
            comment_form.post = post
            comment_form.save()

            return redirect(reverse("post_detail", kwargs={'slug':post.slug}))



# user dashboard for CRUD operations
class DashBoardView(LoginRequiredMixin, CategoryMixin, ListView):
    login_url = 'profiles:login'
    template_name = 'dashboard/dpost_list.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        d_posts = self.get_dposts()
        context['d_posts'] = d_posts
        context['page_obj'] = d_posts
        context['post_form'] = PostForm
        return context


    def get_dposts(self):
        queryset = Post.objects.filter(author_id=self.request.user.profile)
        paginator = Paginator(queryset, 8)
        page = self.request.GET.get('page')
        d_posts = paginator.get_page(page)
        return d_posts



# post delete view
class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'profiles:login'
    model = Post
    template_name = 'dashboard/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

def PostUpdateView(request, slug):
    context={}

    post = get_object_or_404(Post, slug=slug)
    print(post)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        post= form.save(commit=False)
        post.save()
        return redirect('dashboard')
    context = {'post_form':form}

    return render(request, 'dashboard/d_base.html', context)


# post update view
# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     login_url = 'profiles:login'
#     form_class = PostForm
#     model = Post
#     template_name = 'dashboard/d_base.html'
#     success_url = reverse_lazy('dashboard')
#
#     def get_context_data(self, **kwargs):
#         context = super(PostUpdateView, self).get_context_data()
#         context['form'] = PostForm
#         return context
#
#     # def get(self, request, *args, **kwargs):
#     #     post = get_object_or_404(Post, slug=self.slug)
#     #     form = PostForm(request.POST or None, instance=post)
#     #
#     #     if form.is_valid():
#     #         post = form.save(commit=False)
#     #         post.save()
#     #         return redirect('dashboard')
#     #
#









# like post functionality
@login_required
def Like_Post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    is_liked = False
    if post.likes.filter(id=request.user.profile.id).exists():
        post.likes.remove(request.user.profile)
        is_liked = False
    else:
        post.likes.add(request.user.profile)
        is_liked = True

    return HttpResponseRedirect(reverse('post_list'))


#REST API
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer





# @login_required
# def publish_post(request,slug):
#     post = get_object_or_404(Post, slug=slug)
#     post_slug = post.slug
#     post.publish()
#     return redirect('dashboard')



# class CommentCreateView(LoginRequiredMixin, CreateView):
#     login_url = 'profiles:login'
#     model = Comments
#     form_class = CommentForm
#
#     def get_success_URL(self):
#         return reverse('post_detail', kwargs={'slug': self.object.slug})
#
#     def form_valid(self, form):
#         post = get_object_or_404(Post, slug = self.kwargs['slug'] )
#         comment_form = form.save(commit=False)
#         comment_form.author = self.request.user.profile
#         comment_form.post = post
#         comment_form.save()
#
#         return super(CommentCreateView, self).form_valid(form)


# def add_comment_to_post(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     if request.method == "POST":
#
#         form = CommentForm(data=request.POST['comment'])
#         comment_form = form.save(commit=False)
#         try:
#             comment_form.author = request.user.profile
#             comment_form.post = post
#             comment_form.save()
#         except:
#             print('user has no profile')
#
#         return redirect('post_detail', slug=post.slug)
#     return reverse('post_detail', slug=post.slug)
