from django.conf.urls import url
from article import views


urlpatterns = [

    #     Article model
    url(r'^$', views.ArticlesList.as_view()),
    url(r'^single/(?P<pk>[0-9]+)', views.SpecificArticle.as_view()),
    url(r'^category/', views.get_article_by_category),
    url(r'^user/(?P<pk>[0-9]+)', views.get_article_by_user),
    url(r'^mine/',  views.get_my_articles),

    #   Article vote model
    url(r'^vote/', views.Vote.as_view()),

    # reported article
    url(r'^report/', views.ReportedArticlesList.as_view()),

    # bookmark article
    url(r'^bookmarks/', views.BookmarksList.as_view()),
    url(r'^bookmark/(?P<pk>[0-9]+)', views.BookmarksDetail.as_view()),

    # comments to an article
    url(r'^comments/', views.CommentToAnArticleList.as_view()),
    url(r'^comment/(?P<pk>[0-9]+)', views.CommentToAnArticleDetail.as_view()),

    # report a comment
    url(r'^reported/comments', views.ReportedArticleCommentList.as_view()),
]
