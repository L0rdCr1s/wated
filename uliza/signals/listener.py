from django.db.models import signals
from django.dispatch import receiver
from uliza import models as uliza_models
from sautiYangu.models import NotifyUser, Notification
from accounts import models as accounts_models
from django.shortcuts import get_object_or_404
from django.db.models.base import ObjectDoesNotExist


# generic method that creates a notification
def create_notification(text, user, target):
    notification = Notification.objects.create(user=user, text=text)
    notification.save()
    notify_user = NotifyUser.objects.create(user_notification=notification, target_user=target, read=False)
    notify_user.save()


# generic method that creates a notification for multiple users
def create_multi_user_notification(text, instance, targets):
    notification = Notification.objects.create(user=instance.author, text=text)
    notification.save()

    for target in targets:
        notify_user = NotifyUser.objects.create(user_notification=notification,
                                                target_user=target.following, read=False)
        notify_user.save()


# creates notification if a user creates a question
@receiver(signals.post_save, sender=uliza_models.Question)
def question_created(instance, created, **kwargs):
    if created:
        # find the author's full name
        author = None
        try:
            author = accounts_models.UserProfile.objects.get(user=instance.author)
        except ObjectDoesNotExist:
            if author is None:
                author = get_object_or_404(accounts_models.InstituteProfile, institute=instance.author)
        text = "{} created a new question".format(author.get_full_name())
        # find all the targets of the notification
        targets = accounts_models.UserFollow.objects.filter(followed=instance.author)
        create_multi_user_notification(text, instance, targets)

        """
            a user who has asked the question should follow it by default to get notified
            if the new answer is posted on the question
        """
        following = uliza_models.FollowedQuestion.objects.create(question=instance, following=instance.author)
        following.save()


# creates a notification when an answer is made to a question
@receiver(signals.post_save, sender=uliza_models.Answer)
def answer_created(instance, created, **kwargs):
    if created:
        # find the author's full name
        author = None
        try:
            author = accounts_models.UserProfile.objects.get(user=instance.author)
        except ObjectDoesNotExist:
            if author is None:
                author = get_object_or_404(accounts_models.InstituteProfile, institute=instance.author)
        text = "{} answered a question".format(author.get_full_name())
        # find all the targets of the notification
        targets = accounts_models.UserFollow.objects.filter(followed=instance.author)
        create_multi_user_notification(text, instance, targets)

        text = "new answer is posted to {}".format(instance.answered_question.quest_content)
        targets = uliza_models.FollowedQuestion.objects.filter(question=instance.answered_question)
        create_multi_user_notification(text, instance, targets)

        instance.answered_question.answers += 1
        instance.answered_question.save()


# when an answer has been deleted
@receiver(signals.post_delete, sender=uliza_models.Answer)
def answer_deleted(instance, **kwargs):
    instance.answered_question.answers -= 1
    instance.answered_question.save()


# creates notification when a vote has been made on a question
@receiver(signals.post_save, sender=uliza_models.AnswerVote)
def answer_is_voted(instance, created, **kwargs):
    if created:
        user = accounts_models.UserProfile.objects.get(user=instance.user)

        vote = "upvoted"
        if instance.vote == 0:
            vote = "downvoted"
            instance.voted_answer.downvotes += 1
            instance.voted_answer.save()
        elif instance.vote == 1:
            instance.voted_answer.upvotes += 1
            instance.voted_answer.save()

        text = "{} {} your answer".format(user.get_full_name(), vote)
        target = instance.voted_answer.author
        create_notification(text, instance.user, target)


# reduces number of either up votes or down votes if a vote is deleted
@receiver(signals.post_delete, sender=uliza_models.AnswerVote)
def answer_vote_deleted(instance, **kwargs):
    if instance.vote == 0:
        instance.voted_answer.downvotes -= 1
        instance.voted_answer.save()
    elif instance.vote == 1:
        instance.voted_answer.upvotes -= 1
        instance.voted_answer.save()


# creates a notification when a comment to an answer has been made
@receiver(signals.post_save, sender=uliza_models.CommentToAnAnswer)
def answer_commented(instance, created, **kwargs):
    if created:
        # find the author's full name
        user = None
        try:
            user = accounts_models.UserProfile.objects.get(user=instance.author)
        except ObjectDoesNotExist:
            if user is None:
                user = get_object_or_404(accounts_models.InstituteProfile, institute=instance.author)
        text = "{} commented on your answer".format(user.get_full_name())
        target = instance.answer.author
        create_notification(text, instance.author, target)

        # add number of comments to a question
        instance.answer.comments += 1
        instance.answer.save()


# deletes the number of comments when a comment to a question is deleted
@receiver(signals.post_delete, sender=uliza_models.CommentToAnAnswer)
def comment_deleted(instance, **kwargs):
    instance.answer.comments -= 1
    instance.answer.save()


# adds the number of followers if a user follows a question
@receiver(signals.post_save, sender=uliza_models.FollowedQuestion)
def question_followed(instance, created, **kwargs):
    if created:
        instance.question.following += 1
        instance.question.save()


# reduce the number of followers if a user unfollows a question
@receiver(signals.post_delete, sender=uliza_models.FollowedQuestion)
def question_unfollowed(instance, **kwargs):
    instance.question.following -= 1
    instance.question.save()


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


# generic method for creating a report notification and add reports counter by one
def create_a_report_notification(instance_name, report, instance):
    text = "your {} has been reported as {}".format(instance_name, report)
    create_notification(text, instance.author, instance.author)
    instance.reports += 1
    instance.save()

    instance.reports += 1
    instance.save()


# generic method to reduce the number of reports when a report is deleted
def reduce_reports_number(instance):
    instance.reports -= 1
    instance.save()


# creates a notification if an answer is reported
@receiver(signals.post_save, sender=uliza_models.ReportedAnswer)
def answer_reported(instance, created, **kwargs):
    if created:
        report = translate_report(instance.report)
        create_a_report_notification("answer", report, instance.answer)


# reduces number of reports if an answer report has been revoked
@receiver(signals.post_delete, sender=uliza_models.ReportedAnswer)
def answer_report_removed(instance, **kwargs):
    reduce_reports_number(instance.answer)


# creates a notification if an answer comment is reported
@receiver(signals.post_save, sender=uliza_models.ReportedAnswerComment)
def answer_comment_reported(instance, created, **kwargs):
    if created:
        report = translate_report(instance.report)
        create_a_report_notification("comment", report, instance.comment)


# reduces number of reports if a comment report has been revoked
@receiver(signals.post_delete, sender=uliza_models.ReportedAnswerComment)
def answer_comment_report_removed(instance, **kwargs):
    reduce_reports_number(instance.comments)


# creates a notification if the question is reported
@receiver(signals.post_save, sender=uliza_models.ReportedQuestion)
def question_reported(instance, created, **kwargs):
    if created:
        report = translate_report(instance.report)
        create_a_report_notification("question", report, instance.question)


# reduces number of reports if a comment report has been revoked
@receiver(signals.post_delete, sender=uliza_models.ReportedAnswerComment)
def question_report_removed(instance, **kwargs):
    reduce_reports_number(instance.question)
