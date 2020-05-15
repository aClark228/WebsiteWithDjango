from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'music'

urlpatterns = [

    #/music/
    path('', views.IndexView.as_view(), name='index'), # .as_view() treats the class like a function basically

    path('edit_profile/', views.profile, name='edit_profile'),

    path('home/', views.HomeView.as_view(), name='home'),

    path('login/', auth_views.LoginView.as_view(template_name="music/login.html"), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name="music/logout.html"), name='logout'),

    path('register/', views.register, name='register'),

    #/music/id/
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),

    #/music/album/add/
    path('album/add/', views.AlbumCreate.as_view(), name="album-add"),

    #/music/album/pk
    path('album/<int:pk>/edit/', views.AlbumUpdate.as_view(), name="album-update"),

    #/music/album/pk/delete
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name="album-delete"),

    path('song/add/', views.SongCreate.as_view(), name="song-add")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
