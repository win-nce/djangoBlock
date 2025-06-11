from django.urls import path
from django.contrib.auth.views import LogoutView
from app.views import IndexView, CustomLoginView, register, PostDetailView, PostListView, PostDeleteView, PostCreateView, PostUpdateView


urlpatterns = [
    path("", IndexView.as_view(), name="index"), # Главная страица
    path("auth/register", register, name="register"), # registration
    path("auth/login", CustomLoginView.as_view(), name="login"), # authorisation
    path("auth/logout", LogoutView.as_view(next_page="login"), name="logout"), # exit from our login

    # Посты
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"), # Получение Поста     
    path("posts/", PostListView.as_view(), name="post-list"), # Список Постов
    path("posts/delete/<int:pk>", PostDeleteView.as_view(), name="post-delete"), # Удаление Поста
    path("posts/create", PostCreateView.as_view(), name="post-create"), # Содание Поста
    path("posts/update/<int:pk>", PostUpdateView.as_view(), name="post-update"), # Изменение Поста
]