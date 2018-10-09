from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from Sauti_yangu import shared


from article import models as app
from Sauti_yangu.shared import get_serializer


class ArticlesList(APIView):
    rof = ('upvotes', 'downvotes', 'comments', 'reports', 'created_at')
    serializer = get_serializer(app.Article, fields="__all__", rof=rof)

    def get(self, request, format=None):
        return shared.get(request, app.Article, serializer=self.serializer, order_by="-created_at")

    def post(self, request, format=None):
        return shared.post(request, app.Article, serializer=self.serializer, user='author')


class SpecificArticle(APIView):

    def get(self, request, pk, format=None):
        return shared.get_single(request, pk, app.Article)

    def put(self, request, pk, format=None):
        return shared.put(request, pk, app.Article, user='author')

    def delete(self, request, pk, format=None):
        return shared.delete(request, pk, app.Article)


@api_view(['GET', ])
def get_article_by_category(request):
    return shared.get_by_category(request, app.Article)


@api_view(['GET', ])
def get_article_by_user(request, pk):
    return shared.get_by_user(request, pk, app.Article)


@api_view(['GET', ])
def get_my_articles(request):
    return shared.get_my_post(request, app.Article)


"""  Article vote model   """


class Vote(APIView):

    def post(self, request, format=None):

        if request.user.is_authenticated():

            article_id = request.POST.get("id")
            article_vote = None  # to get rid of "variable not initialised" warning
            if request.POST.get("vote") == "upvote":
                article_vote = 1
            elif request.POST.get("vote") == "downvote":
                article_vote = 0

            article = get_object_or_404(app.Article, id=article_id)

            if article.author == request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # check if the user has already made a vote and what kind of vote
            has_vote = app.ArticleVote.objects.filter(user=request.user, voted_article=article).exists()

            if has_vote:
                if article_vote == app.ArticleVote.objects.get(user=request.user, voted_article=article).vote:
                    app.ArticleVote.objects.get(user=request.user, voted_article=article).delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    new_vote = app.ArticleVote.objects.create(user=request.user, vote=article_vote,
                                                              voted_article=article)
                    new_vote.save()
                    if article_vote == 1:
                        article_vote = 0
                    else:
                        article_vote = 1
                    app.ArticleVote.objects.get(user=request.user, voted_article=article,
                                                vote=article_vote).delete()

            else:
                new_vote = app.ArticleVote.objects.create(user=request.user, vote=article_vote,
                                                          voted_article=article)
                new_vote.save()
                return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_403_FORBIDDEN)


""" Reported articles """


class ReportedArticlesList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.ReportedArticle, order_by="-reported_at")

    def post(self, request, format=None):
        shared.post(request, app.ReportedArticle, user=None)


# Bookmark an article


class BookmarksList(APIView):
    serializer = get_serializer(app.BookmarkedArticle, fields="__all__", rof=None)

    def get(self, request, format=None):
        return shared.get_bookmark(request, app.BookmarkedArticle)

    def post(self, request, format=None):
        return shared.post(request, app.BookmarkedArticle, user='bookmark_user')


class BookmarksDetail(APIView):

    def delete(self, request, pk, format=None):
        return shared.delete_bookmark(request, pk, app.BookmarkedArticle)


"""  Comments to an article   """


class ReportedArticleCommentList(APIView):

    def get(self, request, format=None):
        return shared.get(request, app.ReportedArticleComment, order_by="-reported_at")

    def post(self, request, format=None):
        return shared.post(request, app.ReportedArticleComment, user=None)


class CommentToAnArticleList(APIView):
    serializer = get_serializer(app.CommentToAnArticle, fields="__all__", rof=None)

    def get(self, request, format=None):
        article = get_object_or_404(app.Article, id=request.GET.get('id'))
        comments = app.CommentToAnArticle.objects.filter(article=article).order_by("created_at")
        return shared.serialize_many(comments, self.serializer)

    def post(self, request, format=None):
        return shared.post(request, app.CommentToAnArticle, user='user')


class CommentToAnArticleDetail(APIView):

    def put(self, request, pk, format=None):
        return shared.put(request, pk, app.CommentToAnArticle, user='user')

    def delete(self, request, pk, format=None):
        if request.user.is_authenticated():
            comment = get_object_or_404(app.CommentToAnArticle, id=pk)
            if comment.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
