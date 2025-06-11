from django.contrib import admin
from app.models import Post, Like, Dislike, Comment, Report, Media

class CommentInLine(admin.TabularInline):
    model = Comment # Моделька для которой мы делаем Инлайн
    extra = 0 # количестко объектов при создании 

class MediaInLine(admin.StackedInline):
    model = Media
    extra = 2
    max_num = 10 # мак кол-во которое можно создать для определенного поста


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админ панель для модельки поста
    """
    # Помогает видеть столбцы в списке Постов
    list_display = ["pk", "title", "author", "created_at", "get_like_count", "get_comment_count", "get_dislike_count"]
    
    # Помогает нам создать фильтры определенных столбцов:
    list_filter = ["author", "created_at"]
    
    # Помогает реальзовать поиск по определенным столбцам:
    search_fields = ["title"]
    
    # Помогает раизовать пагинацию разделение на страницы:
    list_per_page = 50

    # Подключение Вкладок с привязанными к нашей модели других
    inlines = [CommentInLine, MediaInLine]

    # TODO: Нужно реализовать логику кол-во лайков, дизов и комментов.


    def get_like_count(self, obj):      #obj - наша моделька пост
        """
        метод для подсчета лайков
        :params: Моделька Post
        :return: Кол-во лайков
        """                   
        return obj.likes.count()        #related_name="likes" благодаря related name его название.
    get_like_count.short_description= "Лайки"


    def get_comment_count(self, obj):
        """
        метод для подсчета Комментов
        :params: Моделька Post
        :return: Кол-во Комментов
        """                   
        return obj.comments.count()
    
    get_comment_count.short_description= "Комменты"


    def get_dislike_count(self, obj):
        """
        метод для подсчета Дизов
        :params: Моделька Post
        :return: Кол-во Дизов
        """
        return obj.dislikes.count()
    
    get_dislike_count.short_description= "Дизлайки"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["theme", "post", "user", "is_solve", "created_at"]
    list_filter = ["theme", "user", "is_solve", "created_at"]
    list_per_page = 35


