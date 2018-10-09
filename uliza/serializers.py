from rest_framework import serializers
from uliza import models


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = '__all__'


class AnswerVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnswerVote
        fields = '__all__'


class ReportedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportedQuestion
        fields = '__all__'


class ReportedAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportedAnswer
        fields = '__all__'


class FollowedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FollowedQuestion
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bookmark
        fields = '__all__'


class CommentToAnAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CommentToAnAnswer
        fields = '__all__'


class ReportedAnswerCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportedAnswerComment
        fields = '__all__'