from django.urls import path
from .views import VlogPostListView, VlogPostDetailView, VlogPostCreateView, VlogPostUpdateView, RegisterView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', VlogPostListView.as_view(), name='vlogpost_list'),  # List view for all vlog posts
    path('<int:pk>/', VlogPostDetailView.as_view(), name='vlogpost_detail'),  # Detail view for a specific vlog post
    path('create/', VlogPostCreateView.as_view(), name='vlogpost_create'),  # Create view for adding a new vlog post
    path('<int:pk>/update/', VlogPostUpdateView.as_view(), name='vlogpost_update'),  # Update view for a specific vlog post
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='vlogpost/registration/login.html',
        redirect_authenticated_user=True,
        next_page='vlogpost_list'  # Redirect to the list view after login
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page='vlogpost_list'), name='logout'),  # Built-in logout view
]
