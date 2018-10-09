from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from Sauti_yangu import shared
from uliza import models as app
from Sauti_yangu.shared import get_serializer
from accounts import models as ac_models


class QuestionsList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.Question, order_by="-created_at")

    def post(self, request, format=None):
        return shared.post(request, app.Question, user='author')


class SpecificQuestion(APIView):

    def get(self, request, pk, format=None):
        return shared.get_single(request, pk, app.Question)

    def put(self, request, pk, format=None):
        return shared.put(request, pk, app.Question, user='author')

    def delete(self, request, pk, format=None):
        return shared.delete(request, pk, app.Question)


class AnswerList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.Answer, order_by="created_at")

    def post(self, request, format=None):
        return shared.post(request, app.Answer, user='author')


class SpecificAnswer(APIView):

    def get(self, request, pk, format=None):
        return shared.get_single(request, pk, app.Answer)

    def put(self, request, pk, format=None):
        return shared.put(request, pk, app.Answer, user='author')

    def delete(self, request, pk, format=None):
        return shared.delete(request, pk, app.Answer)


@api_view(['GET', ])
def get_question_by_category(request):
    return shared.get_by_category(request, app.Question)


@api_view(['GET', ])
def get_question_by_user(request, pk):
    return shared.get_by_user(request, pk, app.Question)


@api_view(['GET', ])
def get_answer_by_user(request, pk):
    return shared.get_by_user(request, pk, app.Answer)


@api_view(['GET', ])
def get_my_answers(request):
    return shared.get_my_post(request, app.Answer)


@api_view(['GET', ])
def get_my_questions(request):
    return shared.get_my_post(request, app.Question)


class Vote(APIView):

    def post(self, request, format=None):

        if request.user.is_authenticated():

            answer_id = request.POST.get("id")
            answer_vote = None  # to get rid of "variable not initialised" warning
            if request.POST.get("vote") == "upvote":
                answer_vote = 1
            elif request.POST.get("vote") == "downvote":
                answer_vote = 0

            answer = get_object_or_404(app.Answer, id=answer_id)

            if answer.author == request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # check if the user has already made a vote and what kind of vote
            has_vote = app.AnswerVote.objects.filter(user=request.user, voted_answer=answer).exists()

            if has_vote:
                if answer_vote == app.AnswerVote.objects.get(user=request.user, voted_answer=answer).vote:
                    app.AnswerVote.objects.get(user=request.user, voted_answer=answer).delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    new_vote = app.AnswerVote.objects.create(user=request.user, vote=answer_vote, voted_answer=answer)
                    new_vote.save()
                    if answer_vote == 1:
                        answer_vote = 0
                    else:
                        answer_vote = 1
                    app.AnswerVote.objects.get(user=request.user, voted_answer=answer, vote=answer_vote).delete()

            else:
                new_vote = app.AnswerVote.objects.create(user=request.user, vote=answer_vote, voted_answer=answer)
                new_vote.save()
                return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_403_FORBIDDEN)


class ReportedQuestionList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.ReportedQuestion, order_by="-reported_at")

    def post(self, request, format=None):
        return shared.post(request, app.ReportedQuestion, user=None)


class ReportedAnswerList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.ReportedAnswer, order_by="-reported_at")

    def post(self, request, format=None):
        return shared.post(request, app.ReportedAnswer, user=None)


class BookmarksList(APIView):

    def get(self, request, format=None):
        return shared.get_bookmark(request, app.Bookmark)

    def post(self, request, format=None):
        return shared.post(request, app.Bookmark, user='bookmark_user')


class BookmarksDetail(APIView):

    def delete(self, request, pk, format=None):
        return shared.delete_bookmark(request, pk, app.Bookmark)


class CommentToAnAnswerList(APIView):
    serializer = get_serializer(app.CommentToAnAnswer, fields="__all__", rof=None)

    def get(self, request, pk, format=None):
        answer = get_object_or_404(app.Answer, id=pk)
        comments = app.CommentToAnAnswer.objects.filter(answer=answer).order_by("created_at")
        return shared.serialize_many(comments, self.serializer)

    def post(self, request, pk, format=None):
        return shared.post(request, app.CommentToAnAnswer, user='author')


class CommentToAnAnswerDetail(APIView):

    def put(self, request, pk, format=None):
        return shared.put(request, pk, app.CommentToAnAnswer, user='author')

    def delete(self, request, pk, format=None):
        if request.user.is_authenticated():
            comment = get_object_or_404(app.CommentToAnAnswer, id=pk)
            if comment.author != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ReportedAnswerCommentList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.ReportedAnswerComment, order_by="-reported_at")

    def post(self, request, format=None):
        return shared.post(request, app.ReportedAnswerComment, user=None)


class FollowedQuestionLis(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.FollowedQuestion, order_by='-followed_at')

    def post(self, request, format=None):
        return shared.post(request, app.FollowedQuestion, user='following')


class FollowedQuestionDetail(APIView):

    def get(self, request, pk, format=None):
        return shared.get_single(request, pk, app.FollowedQuestion)

    def delete(self, request, pk, format=None):
        if request.user.is_authenticated():
            post = get_object_or_404(app.FollowedQuestion, id=pk)
            if post.following != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', ])
def get_following_by_user(request, pk):
    user = get_object_or_404(ac_models.CustomUser, id=pk)
    data = app.FollowedQuestion.objects.filter(following=user).order_by("-followed_at")
    serializer = get_serializer(app.FollowedQuestion, fields="__all__", rof=None)
    return shared.serialize_many(data, serializer)


@api_view(['GET', ])
def get_my_following(request, pk):
    if request.user.is_authenticated():
        data = app.FollowedQuestion.objects.filter(following=request.user).order_by("-created_at")
        serializer = get_serializer(app.FollowedQuestion, fields="__all__", rof=None)
        return shared.serialize_many(data, serializer)
    return Response(status=status.HTTP_403_FORBIDDEN)