from django.db import models
from accounts.models import CustomUser as user
from django.utils import timezone
from ckeditor.fields import RichTextField


def help_limit(character_limit):
        text = "you are limited to" + character_limit + "characters"
        return text


class Article(models.Model):
    """ This is a Article table"""
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, default='None')
    title = models.CharField(max_length=150)
    content = RichTextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    reports = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title


class ArticleVote(models.Model):
    """ This table handles upvotes and downvotes on an article """
    # vote choices
    down_vote = 0
    up_vote = 1
    vote_choice = [(down_vote, 'downvote'), (up_vote, 'upvote')]

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=vote_choice, db_index=True)
    voted_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    class Meta:
        indexes = [
            models.Index(fields=['voted_article']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.user.get_full_name()


def get_report_choices():
    offensive = 0
    repeated = 1
    out_of_topic = 2
    not_help_full = 3
    report_choices = [
        (offensive, 'Offensive'),
        (repeated, 'Repeated'),
        (out_of_topic, 'Out of topic'),
        (not_help_full, 'Not helpful')
    ]

    return report_choices


class ReportedArticle(models.Model):
    """ a table to hold reported Articles """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    report = models.IntegerField(choices=get_report_choices())
    report_reason = models.CharField(max_length=100, help_text=help_limit('100'))
    reported_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['article']),
            models.Index(fields=['report']),
            models.Index(fields=['reported_at'])
        ]

    def __str__(self):
        return self.report_reason


class BookmarkedArticle(models.Model):
    """ Bookmarking an article, an Article will be followed """
    bookmarked_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    bookmark_user = models.ForeignKey(user, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['bookmark_user']),
        ]

    def __str__(self):
        return self.bookmark_user.get_full_name()


class CommentToAnArticle(models.Model):
    """ Add a comment to a Article """
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self):
        return self.user.get_full_name()


class ReportedArticleComment(models.Model):
    """ A reported comment """

    comment = models.ForeignKey(CommentToAnArticle, on_delete=models.CASCADE)
    report = models.IntegerField(choices=get_report_choices())
    report_reason = models.CharField(max_length=100, help_text=help_limit('100'))
    reported_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['comment']),
            models.Index(fields=['report']),
            models.Index(fields=['reported_at'])
        ]

    def __str__(self):
        return self.report_reason

