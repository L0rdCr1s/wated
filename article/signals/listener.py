from sautiYangu.models import Notification, NotifyUser
from article import models as article_models
from django.db.models import signals
from django.dispatch import receiver
from accounts import models as accounts_models
from django.shortcuts import get_object_or_404
from django.db.models.base import  ObjectDoesNotExist


# generic method that creates a notification
def create_notification(text, user, target):
    notification = Notification.objects.create(user=user, text=text)
    notification.save()
    notify_user = NotifyUser.objects.create(user_notification=notification, target_user=target, read=False)
    notify_user.save()


# creates a notification if the user creates a new article
@receiver(signals.post_save, sender=article_models.Article)
def created_article(instance, created, **kwargs):
    if created:
        # find the author's full name
        author = None
        try:
            author = accounts_models.UserProfile.objects.get(user=instance.author)
        except ObjectDoesNotExist:
            if author is None:
                author = get_object_or_404(accounts_models.InstituteProfile, institute=instance.author)

        # notification text
        if author is not None:
            text = "{} created a new article".format(author.get_full_name())
            notification = Notification.objects.create(user=instance.author, text=text)
            notification.save()

        targets = accounts_models.UserFollow.objects.filter(followed=instance.author)
        if targets is not None:
            for target in targets:
                notify_user = NotifyUser.objects.create(user_notification=notification,
                                                        target_user=target.following, read=False)
                notify_user.save()


# creates a notification if the user comments to an article
@receiver(signals.post_save, sender=article_models.CommentToAnArticle)
def article_commented(instance, created, **kwargs):
    if created:
        # add the number of comments on an article
        instance.article.comments += 1
        instance.article.save()

        # find the author's full name
        author = None
        try:
            author = accounts_models.UserProfile.objects.get(user=instance.user)
        except ObjectDoesNotExist:
            if author is None:
                author = get_object_or_404(accounts_models.InstituteProfile, institute=instance.user)

        text = "{} commented on your article".format(author.get_full_name())
        create_notification(text, instance.user, instance.article.author)


# reduces comments count on an article if a comment is deleted
@receiver(signals.post_delete, sender=article_models.CommentToAnArticle)
def article_comment_deleted(instance, **kwargs):
    instance.article.comments -= 1
    instance.article.save()


# creates a notification when a vote to an article is made
@receiver(signals.post_save, sender=article_models.ArticleVote)
def article_voted(instance, created, **kwargs):
    if created:
        # find the user's full name
        author = None
        try:
            author = accounts_models.UserProfile.objects.get(user=instance.user)
        except ObjectDoesNotExist:
            if author is None:
                author = get_object_or_404(accounts_models.InstituteProfile, institute=instance.user)

        vote = "upvoted"
        if instance.vote == 0:
            vote = "downvoted"
            instance.voted_article.downvotes += 1
            instance.voted_article.save()
        elif instance.vote == 1:
            instance.voted_article.upvotes += 1
            instance.voted_article.save()

        text = "{} {} your article".format(author.get_full_name(), vote)
        create_notification(text, instance.user, instance.voted_article.author)


# reduces number of either up votes or down votes if a vote is deleted
@receiver(signals.post_delete, sender=article_models.ArticleVote)
def article_vote_deleted(instance, **kwargs):
    if instance.vote == 0:
        instance.voted_article.downvotes -= 1
        instance.voted_article.save()
    elif instance.vote == 1:
        instance.voted_article.upvotes -= 1
        instance.voted_article.save()


def translate_report(report):
    if report == 0:
        report = "offensive"
    elif report == 1:
        report = "repeated"
    elif report == 2:
        report = "out of topic"
    elif report == 3:
        report = "not helpful"

    return report


# creates a notification when an article is reported
@receiver(signals.post_save, sender=article_models.ReportedArticle)
def article_reported(instance, created, **kwargs):
    if created:
        instance.article.reports += 1
        instance.article.save()
        report = translate_report(instance.report)

        text = "your article is reported as {}".format(report)
        create_notification(text, instance.article.author, instance.article.author)


# reduces number of reports if a report is on an article is deleted
@receiver(signals.post_delete, sender=article_models.ReportedArticle)
def article_report_deleted(instance, **kwargs):
    instance.article.reports -= 1
    instance.article.save()


# creates a notification when an article comment is reported
@receiver(signals.post_save, sender=article_models.ReportedArticleComment)
def article_comment_reported(instance, created, **kwargs):
    if created:
        report = translate_report(instance.report)

        text = "your comment is reported as {}".format(report)
        create_notification(text, instance.comment.user, instance.comment.user)


# creates notification if a user has followed another user
@receiver(signals.post_save, sender=accounts_models.UserFollow)
def user_is_followed(instance, created, **kwargs):
    if created:
        following = None
        try:
            following = accounts_models.UserProfile.objects.get(user=instance.following)
        except ObjectDoesNotExist:
            if following is None:
                following = get_object_or_404(accounts_models.InstituteProfile, institute=instance.following)

        text = "{} is following you".format(following.get_full_name())
        create_notification(text, instance.following, instance.followed)
