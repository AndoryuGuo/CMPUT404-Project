from Accounts.models import Author
from Accounts.models import Friendship
from posting.models import Post, Comment
from django.db import models
from rest_framework import serializers
import json

#Author serializer for GET, PUT author profile
class AuthorSerializer(serializers.ModelSerializer):
    #author fields
    #author model doesn't need to store url, which gonna be moved to serializer
    url = serializers.SerializerMethodField()
    class Meta:
        model = Author
        #fields = '__all__'
        fields = ('id', 'bio', 'displayName', 'github', 'url')

    def get_url(self, obj):
        return "{}/author/{}".format(obj.host, obj.id)

# Helper serializer for the api/author/{author_id}
class Helper_AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')

# Helper serializer for the api/author/{authod_id}
class Helper_AuthorFriendSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return Helper_AuthorSerializers(obj.recv_id).data

    class Meta:
        model = Friendship
        fields = ("author",)
# Serializer for the api/author/{author_id}
class ExtendAuthorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')


class Helper_FollowingSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return obj.recv_id.id

    class Meta:
        model = Friendship
        fields = ("author",)


class FollowingSerializers(serializers.ModelSerializer):
    friends = Helper_FollowingSerializers(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ('friends',)


class Helper_FollowerSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return obj.init_id.id

    class Meta:
        model = Friendship
        fields = ("author",)

class FollowerSerializers(serializers.ModelSerializer):
    follower = Helper_FollowerSerializers(many=True, read_only=True)
    class Meta:
        model = Friendship
        fields = ('follower',)


#reference: https://www.django-rest-framework.org/api-guide
class PostSerializer(serializers.ModelSerializer):
    #override some fields
    #author = AuthorSerializer(read_only=True)
    #comments = serializers.SerializerMethodField()
    #Todo:
    #  count
    #  size
    #  ...
    postauthor = serializers.SerializerMethodField('get_author')
    def get_author(self, obj):
        return Helper_AuthorSerializers(Author.objects.get(id=obj.author.id)).data


    class Meta:
        model = Post
        fields = ('postid', 'postauthor', 'title', 'source', 'origin', 'description', 'contentType', 'published', 'content','visibility','visibleTo','unlisted')

    def get_comment(self, obj):
        comments = Comment.objects.filter(post=obj.postid).order_by('published')    # pylint: disable=maybe-no-member
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def create(self, validated_data):
        #for fields which are no belonged to, might need to pop that data
        author = self.context['author']
        origin = self.context['origin']
        post = Post.objects.create(author=author, origin=origin, source=origin, **validated_data)  # pylint: disable=maybe-no-member
        src = origin+'/'+str(post.postid)+'/'    # pylint: disable=maybe-no-member
        post.source = post.origin = src
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.source = validated_data.get('source', instance.source)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    # def create(self, validated_data):
    #     author = self.context['author']
    #     post = self.context['post']
    #     return Comment.objects.create(author=author, post=post, **validated_data)
