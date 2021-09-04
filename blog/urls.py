from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.SearchPostView.as_view(), name='search_result'),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),

    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<slug:slug>/', views.PostUpdateView, name='post_update'),
    path('like/<slug:slug>', views.Like_Post, name = 'like_post'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
