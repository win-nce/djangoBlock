from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from app.models import Post, Dislike, Like, Report
from app.forms import PostForm, CustomUserCreationForm, CommentForm

# TODO: Сделать Cтраницу Главную Index
class IndexView(ListView):
    """
    Представление для Главной Страницы
    """
    # Для подключения модельки
    model = Post
    # Устанавливаем Шаблон HTML 
    template_name = "app/index.html"
    # Имя перемнной в Шаблоне
    context_object_name = "posts"
    # Сортировка по какому либо полю либо сортировка нескольких полей
    ordering = ["-created_at"] # по убыванию
    # Для реалзации Пагинации
    paginate_by = 30


# TODO: Сделать Cтраницу Создание Поста
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представления для Создания Поста
    Но посты могут создавать только Авторизованные пользователи
    """
    # Для подключения модельки чтоб знать объект какой модельки он должен создать
    model = Post
    # Для создания Поста нужно указывать форму 
    form_class = PostForm
    # Шаблон HTML
    template_name = "app/post_form.html"
    # Куда перенаправлять после создания
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.author = self.request.user    # мы в ручную указываем что юзер - наш автор
        return super().form_valid(form)


# TODO: Сделать Cтраницу Списка Постов
class PostListView(ListView):
    """
    Представление для Списка Постов
    """
    # Для подключения модельки
    model = Post
    # Устанавливаем Шаблон HTML 
    template_name = "app/post_list.html"
    # Имя перемнной в Шаблоне
    context_object_name = "posts"
    # Сортировка по какому либо полю либо сортировка нескольких полей
    ordering = ["-created_at"] # по убыванию
    # Для реалзации Пагинации
    paginate_by = 50

# TODO: Сделать Cтраницу Просмотра Поста
class PostDetailView(DetailView):
    """
        Представления для Получения одного конкретного Поста
    """
    # Моделька
    model = Post
    # Шаблон HTML
    template_name = "app/post_detail.html"
    # иимя переменной в Шаблон
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Помогает засунуть доп переменные
        """
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm # добавили переменную comment_form
        return context

# TODO: Сделать Cтраницу Изменение Поста
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "app/post_form.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy("post-detail", pk=self.object.pk)
    
    def test_func(self):
        """
        Проверка того что пользователь - автор
        """
        post = self.get_object()
        return self.request.user == post.author
    
# TODO: Сделать Cтраницу Подтверждение Удаления
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy("post-list")

    def test_func(self):
        """
        Проверка того что пользователь - автор и он имеет право удалять
        """
        post = self.get_object()
        return self.request.user == post.author


# TODO: сделать РЕГ/Авторизация
# TODO: Регистрация
def register(request):
    if request.method == "POST": # Пользователь зашел на страницу и заполнил форму
        form = CustomUserCreationForm(request.POST) # Тут вставили в форму данные которые дал пользователь
        if form.is_valid(): # Проверили пользователя
            user = form.save() # Сохранили пользователя
            return redirect("login")
    else: # Пользователь только зашел на страницу
        form = CustomUserCreationForm() # Отправили пустую форму пользователю что бы он ее заполнил
    return render(
        request,
        "app/register.html",
        {
            "form": form
        }
    )

# TODO: Авторизация
class CustomLoginView(LoginView):
    template_name = "app/login.html"
    success_url = reverse_lazy("index")


@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)

        # Удаление дизлайка
        Dislike.objects.filter(post=post, user=request.user).delete()
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()

        return redirect("post-detail", post_id)

@login_required
def dislike_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)

        # Удаление лайка
        Like.objects.filter(post=post, user=request.user).delete()
        dislike, created = Dislike.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            dislike.delete()

        return redirect("post-detail", post_id)

@login_required
def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user # Вручную указали Пользователя который создал коммент
            comment.post = post # Вручную указали Пост которому создали коммент
            comment.save() #сохранили коммент
            return redirect("post-detail", post_id)
        else:
            return redirect("post-detail", post_id)
    else:
        return redirect("post-detail", post_id)

def about_us(request):
    pass

# TODO: Сделать Cтраницу Создание Жалоб
def create_report(request, post_id):
    pass


# TODO: Сделать Cтраницу Список жалоб Пользователя
class RepostListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "app/report_list.html"
    context_object_name = "reports"

    def get_queryset(self): # Фильтруем данные
        # сделали так чтобы пользователь видел только свои жалобы
        return Report.objects.filter(user=self.request.user)