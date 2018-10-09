from django.db import models
from accounts.models import CustomUser as user
from django.utils import timezone
from ckeditor.fields import RichTextField


def help_limit(character_limit):
        text = "you are limited to" + character_limit + "characters"
        return text


class Question(models.Model):
    """ This is a question table"""
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, default='None')
    quest_content = models.CharField(max_length=255, help_text=help_limit('255'))
    description = models.CharField(max_length=300, help_text=help_limit('300'))
    created_at = models.DateTimeField(default=timezone.now)
    following = models.PositiveIntegerField(default=0)
    answers = models.PositiveIntegerField(default=0)
    reports = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['quest_content'])
        ]

    def __str__(self):
        return self.quest_content


class Answer(models.Model):
    """ This is the answers table """
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    answered_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(default=timezone.now)
    comments = models.PositiveIntegerField(default=0)
    reports = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['answered_question'])
        ]

    def __str__(self):
        return self.answered_question.quest_content


class AnswerVote(models.Model):
    """ This table handles upvotes and downvotes on an answer """
    # vote choices 
    down_vote = 0
    up_vote = 1
    vote_choice = [(down_vote, 'downvote'), (up_vote, 'upvote')]

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=vote_choice, db_index=True)
    voted_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['voted_answer']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.user.get_full_name()


class ReportedQuestion(models.Model):
    """ a table to hold reported questions """
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

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    report = models.IntegerField(choices=report_choices)
    report_reason = models.CharField(max_length=100, help_text=help_limit('100'))
    reported_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['report']),
            models.Index(fields=['reported_at'])
        ]

    def __str__(self):
        return self.question.quest_content


class ReportedAnswer(models.Model):
    """ a table to hold reported questions """
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

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    report = models.IntegerField(choices=report_choices)
    report_reason = models.CharField(max_length=100, help_text=help_limit('100'))
    reported_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['answer']),
            models.Index(fields=['report']),
            models.Index(fields=['reported_at'])
        ]

    def __str__(self):
        return self.report_reason


class FollowedQuestion(models.Model):
    """ This is the table for the followed questions """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    following = models.ForeignKey(user, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['following']),
            models.Index(fields=['followed_at'])
        ]

    def __str__(self):
        return self.following.get_full_name()


class Bookmark(models.Model):
    """ Bookmarking an answer, a question will be followed """
    bookmarked_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    bookmark_user = models.ForeignKey(user, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['bookmark_user']),
        ]

    def __str__(self):
        return self.bookmark_user.get_full_name()


"""
class CommentToAQuestion(models.Model):
    # Add a comment to a question 
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()


class ReportedQuestionComment(models.Model):
    # A reported comment 
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

    comment = models.ForeignKey(CommentToAQuestion, on_delete=models.CASCADE)
    report = models.IntegerField(choices=report_choices, db_index=True)
    report_reason = models.CharField(max_length=100, help_text=help_limit('100'))
    reported_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['comment']),
            models.Index(fields=['report']),
            models.Index(fields=['reported_at'])
        ]

    def __str__(self):
        return self.report_reason
"""


class CommentToAnAnswer(models.Model):
    """ Add a comment to an answer """
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(default=timezone.now)
    reports = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.author.get_full_name()


class ReportedAnswerComment(models.Model):
    """ A reported comment """
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

    comment = models.ForeignKey(CommentToAnAnswer, on_delete=models.CASCADE)
    report = models.IntegerField(choices=report_choices)
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
