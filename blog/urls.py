from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashBoardView.as_view(), name='post_drafts'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('search/', views.SearchPostView.as_view(), name='search_result'),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail')

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
