from django.conf.urls import url
from uliza import views

urlpatterns = [

    # Answer

    url(r'^answer/single/(?P<pk>[0-9]+)', views.SpecificAnswer.as_view()),
    url(r'^answer/user/(?P<pk>[0-9]+)', views.get_answer_by_user),
    url(r'^answer/mine/', views.get_my_answers),

    # Question

    url(r'^question/single/(?P<pk>[0-9]+)', views.SpecificQuestion.as_view()),
    url(r'^question/category/', views.get_question_by_category),
    url(r'^question/user/(?P<pk>[0-9]+)', views.get_question_by_user),
    url(r'^question/mine/', views.get_my_questions),

    # Answer vote
    url(r'^vote/', views.Vote.as_view()),

    # reports
    url(r'^answer/report/', views.ReportedAnswerList.as_view()),
    url(r'^answer/comment/report/', views.ReportedAnswerCommentList.as_view()),
    url(r'^question/report/', views.ReportedQuestionList.as_view()),

    # bookmark
    url(r'^bookmarks/', views.BookmarksList.as_view()),
    url(r'^bookmark/(?P<pk>[0-9]+)', views.BookmarksDetail.as_view()),

    # comments
    url(r'^answer/comments/(?P<pk>[0-9]+)', views.CommentToAnAnswerList.as_view()),
    url(r'^answer/comment/(?P<pk>[0-9]+)', views.CommentToAnAnswerDetail.as_view()),

    # followed question
    url(r'^question/following', views.FollowedQuestionLis.as_view()),
    url(r'^question/single/following/(?P<pk>[0-9]+)', views.FollowedQuestionDetail.as_view()),
    url(r'^question/user/following/(?P<pk>[0-9]+)', views.get_following_by_user),
    url(r'^question/mine/following/', views.get_my_following),

    url(r'^answer', views.AnswerList.as_view()),
    url(r'^question', views.QuestionsList.as_view()),
]