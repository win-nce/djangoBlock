from django.db import models
from django.contrib.auth.models import User

# Posts
class Post(models.Model):
    """
    Моделька постов, будут храниться все посты пользователей.

    Attributes:
        title: Поле название Поста макс символов 256 символов,
        content: Поле Контента Поста макс символов 3000 символов,
        created_at: Полу даты Создания автоматически определяет время создания,
        author: Поле Автор привязан к модели Пользователь(User),
    """
    title = models.CharField(max_length=256, verbose_name="Название Поста")
    content = models.CharField(max_length=3000, verbose_name="Контент Поста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title
    
    # Метод учета лайков
    def get_likes_count(self):
        return self.likes.count()   #likes взяли от related name
    
    # Метод учета дизлайков
    def get_dislikes_count(self):
        return self.dislikes.count()

    # Метод учета комментов
    def get_comments_count(self):
        return self.comments.count()
    
    # Метод доставания первого изображения
    def get_first_media(self):
        return self.media.order_by("created_at").first()

    class Meta:
        verbose_name_plural = "Посты"


# Comments
class Comment(models.Model):
    """
        Моделька Комментыб она привязана к посту, у каждого поста будет коммертарии

        Attributes:
            post: Пост которому был написан коммент,
            body: Содержимое Коммента,
            user: Пользователь который написал Комментарий,
            created_at: Время когда был написан Комментарий.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост")
    body = models.CharField(max_length=1000, verbose_name='Содержимое')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания Комментария")

    def __str__(self):
        return f"{self.post.title}-{self.user.username}"

    class Meta:
        verbose_name_plural = "Комментарии"


# Likes
class Like(models.Model):
    """
        Моделька для подсчета Лайков Постов

        Attributes:
            post: Пост которому поставили Лайк,
            user: Пользователь который поставил Лайк,
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="likes", verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

# Dislikes
class Dislike(models.Model):
    """
        Моделька для подсчета Дизлайков Постов

        Attributes:
            post: Пост которому поставили Дизлайк,
            user: Пользователь который поставил Дизлайк,
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="dislikes", verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

# Report(Жалобы)
class Report(models.Model):
    """
        Моделька для репорта Жалоб на посты
        
        Attributes:
            theme: Тема Жалоб,
            post: Пост на который Пожаловались,
            user: Юзер который Пожаловался,
            description: Описание жалобы,
            created_at: Время Жалобы,
            is_solve: Решена ли Жалоба?
    """
    # Choise
    THEMES = (
        ("NI", "Неинтересно"),
        ("CE", "Цензура"),
        ("SP", "Спам"),
        ("OT", "Другое"),
    )

    theme = models.CharField(max_length=3, choices=THEMES) #max_length=3 три только потому что в будущем можем и другое написать а не только двузначное.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    description = models.CharField(max_length=1024, verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания Жалобы")
    is_solve = models.BooleanField(default=False, verbose_name="Решена")

    def __str__(self):
        return f"{self.post.title}-{self.user.username}-{self.theme}"

    class Meta:
        verbose_name_plural = "Жалобы"


# Media
class Media(models.Model):
    """
    Моделька для Медиафайлов Постов

    Attributes:
        post: Пост к которому привязан Медиафайл,
        created_at: Время создания Медиафайла,
        url: Ссылка на изображение,
        file: Сам файл.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media", verbose_name="Пост")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания Медиафайла")
    url = models.URLField(null=True, blank=True, verbose_name="Ссылка")
    file = models.ImageField(upload_to="post-gallery/", null=True, blank=True) # jpg jpeg png webp только изображения

    class Meta:
        verbose_name_plural = "Медиа"
