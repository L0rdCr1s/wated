from django.contrib import admin
from .models import (
    Article, ArticleVote, ReportedArticle, BookmarkedArticle,
    CommentToAnArticle, ReportedArticleComment,
)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('category', 'author', 'created_at',
                    'upvotes', 'downvotes', 'comments', 'reports')
    list_filter = ('author', 'created_at')
    ordering = ('upvotes',)
    search_fields = ('category', 'author')


admin.site.register(Article, ArticleAdmin)


class ArticlesVotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'vote', 'voted_at', 'voted_article')
    list_filter = ('user', 'voted_at')
    ordering = ('user',)
    search_fields = ('user',)
    # readonly_fields = ('vote', 'voted_at', 'user', 'voted_article')


admin.site.register(ArticleVote, ArticlesVotesAdmin)


class ReportedArticleAdmin(admin.ModelAdmin):
    list_display = ('report', 'reported_at', 'article', 'report_reason')
    list_filter = ('reported_at', 'article')
    ordering = ('article',)
    search_fields = ('article',)
    # readonly_fields = ('report', 'reported_at', 'article', 'report_reason')


admin.site.register(ReportedArticle, ReportedArticleAdmin)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('bookmarked_article', 'bookmark_user', 'created_at')
    list_filter = ('bookmarked_article', 'bookmark_user')
    ordering = ('bookmark_user',)
    search_fields = ('bookmark_user',)


admin.site.register(BookmarkedArticle, BookmarkAdmin)


class CommentToAnArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('user', 'created_at')
    ordering = ('created_at',)
    search_fields = ('user', 'content',)


admin.site.register(CommentToAnArticle, CommentToAnArticleAdmin)


class ReportedArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'report', 'reported_at', 'report_reason')
    list_filter = ('reported_at', 'report')
    ordering = ('reported_at',)
    search_fields = ('comment', 'report',)


# reported Article comment and reported answer comment share the same fields
# so they are all registered with same model admin
admin.site.register(ReportedArticleComment, ReportedArticleCommentAdmin)

