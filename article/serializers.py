
"""

    THIS CODE IS COMMENTED BECAUSE THERE IS A LOT OF CODE REPEATING
    IT IS NOT DELETED BECAUSE A CUSTOM THING MIGHT BE NEEDED FOR A SPECIFIC CLASS SERIALIZER 
    
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Article
        fields = '__all__'
        read_only_fields = ('upvotes', 'downvotes', 'comments', 'reports', 'created_at')


class ArticleVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArticleVote
        fields = '__all__'
        read_only_fields = ('voted_at', 'voted_article')


class ReportedArticleSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.ReportedArticle
        fields = "__all__"


class BookmarksSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.BookmarkedArticle
        fields = "__all__"


class CommentToAnArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CommentToAnArticle
        fields = "__all__"


class ReportedArticleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportedArticleComment
        fields = "__all__"""""