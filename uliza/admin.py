from django.contrib import admin
from .models import (
    Answer, Question, AnswerVote,
    ReportedAnswer, ReportedQuestion,
    FollowedQuestion, Bookmark, CommentToAnAnswer,
    ReportedAnswerComment,
)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'author', 'created_at', 'following', 'answers', 'reports')
    list_filter = ('author', 'created_at')
    ordering = ('created_at',)
    search_fields = ('category', 'author')


admin.site.register(Question, QuestionAdmin)


# answer shares some of the fields with question
class AnswerAdmin(QuestionAdmin):
    list_display = ('author', 'created_at', 'answered_question',
                     'comments', 'reports', 'upvotes', 'downvotes')
    search_fields = ('author',)


admin.site.register(Answer, AnswerAdmin)


# answers vote shares some of the fields with question vote model
class AnswersVotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'vote', 'voted_at', 'voted_answer')
    list_filter = ('user', 'voted_at')
    ordering = ('user',)
    search_fields = ('user',)
    # readonly_fields = ('vote', 'voted_at', 'user', 'voted_answer')


admin.site.register(AnswerVote, AnswersVotesAdmin)


class ReportedAnswersAdmin(admin.ModelAdmin):
    list_display = ('report', 'reported_at', 'answer', 'report_reason')
    list_filter = ('reported_at', 'answer')
    ordering = ('answer',)
    search_fields = ('answer',)
    # readonly_fields = ('report', 'reported_at', 'answer', 'report_reason')


admin.site.register(ReportedAnswer, ReportedAnswersAdmin)


class ReportedQuestionAdmin(admin.ModelAdmin):
    list_display = ('report', 'reported_at', 'question', 'report_reason')
    list_filter = ('reported_at', 'question')
    ordering = ('question',)
    search_fields = ('question',)
    # readonly_fields = ('report', 'reported_at', 'question', 'report_reason')


admin.site.register(ReportedQuestion, ReportedQuestionAdmin)


class FollowedQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'following', 'followed_at')
    list_filter = ('followed_at', 'question', 'following')
    ordering = ('following',)
    search_fields = ('question', 'following')
    # readonly_fields = ('report', 'followed_at', 'question', 'report_reason')


admin.site.register(FollowedQuestion, FollowedQuestionAdmin)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('bookmarked_answer', 'bookmark_user', 'created_at')
    list_filter = ('bookmarked_answer', 'bookmark_user')
    ordering = ('bookmark_user',)
    search_fields = ('bookmark_user',)


admin.site.register(Bookmark, BookmarkAdmin)

"""
    class CommentToAQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')
    list_filter = ('user', 'created_at')
    ordering = ('created_at',)
    search_fields = ('user', 'content',)


admin.site.register(CommentToAQuestion, CommentToAQuestionAdmin)
"""


# comment to an answer share some of the fields with the comment to an
# answer model
class CommentToAnAnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'answer', 'created_at')
    list_filter = ('author', 'created_at')
    ordering = ('created_at',)
    search_fields = ('author', 'content',)


admin.site.register(CommentToAnAnswer, CommentToAnAnswerAdmin)


# reported question comment and reported answer comment share the same fields
# so they are all registered with same model admin
class ReportedQuestionCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'report', 'reported_at', 'report_reason')
    list_filter = ('reported_at', 'report')
    ordering = ('reported_at',)
    search_fields = ('comment', 'report',)


# admin.site.register(ReportedQuestionComment, ReportedQuestionCommentAdmin)
admin.site.register(ReportedAnswerComment, ReportedQuestionCommentAdmin)
