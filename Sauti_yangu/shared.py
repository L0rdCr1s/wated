from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from accounts import models as ac_models


# serialize multiple query sets and return Json response ( helper method )
def serialize_many(data, serializer):
    if not data:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_data = serializer(data, many=True)
    return Response(serialized_data.data)


# serialize single query and return Json response ( helper method )
def serialize_single(data, serializer):
    if not data:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_data = serializer(data)
    return Response(serialized_data.data)


def get_serializer(serialized_model, **kwargs):

    class MainSerializer(serializers.ModelSerializer):

        class Meta:
            model = serialized_model
            fields = kwargs['fields']
            read_only_fields = kwargs['rof']
    return MainSerializer


def get(request, model, serializer=None, order_by=None):
    if serializer is None:
        serializer = get_serializer(model, fields="__all__", rof=None)
    data = model.objects.all().order_by(order_by)
    return serialize_many(data, serializer)


def get_single(request, pk, model, serializer=None):
    if serializer is None:
        serializer = get_serializer(model, fields="__all__", rof=None)
    data = get_object_or_404(model, id=pk)
    return serialize_single(data, serializer)


def post(request, model, serializer=None, **kwargs):
    if serializer is None:
        serializer = get_serializer(model, fields="__all__", rof=None)
    if request.user.is_authenticated():
        if kwargs['user'] is not None:
            user = kwargs['user']
            request.data[user] = request.user.id
        deserialized_data = serializer(data=request.data)

        if deserialized_data.is_valid():
            deserialized_data.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_403_FORBIDDEN)


def put(request, pk, model, serializer=None, **kwargs):
    if serializer is None:
        serializer = get_serializer(model, fields="__all__", rof=None)
    if request.user.is_authenticated():
        data = get_object_or_404(model, id=pk)
        if data.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = kwargs['user']
        request.data[user] = request.user.id
        serialized_data = serializer(data, data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)

        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


def delete(request, pk, model):
    if request.user.is_authenticated():
        data = get_object_or_404(model, id=pk)
        if data.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)


def delete_bookmark(request, pk, model):
    if request.user.is_authenticated():
        data = get_object_or_404(model, id=pk)
        if data.bookmark_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)


def get_by_category(request, model):
    cat = request.GET.get("category")
    data = model.objects.filter(category=cat).order_by("-created_at")
    serializer = get_serializer(model, fields="__all__", rof=None)
    return serialize_many(data, serializer)


def get_by_user(request, pk, model):
    user = get_object_or_404(ac_models.CustomUser, id=pk)
    data = model.objects.filter(author=user).order_by("-created_at")
    serializer = get_serializer(model, fields="__all__", rof=None)
    return serialize_many(data, serializer)


def get_my_post(request, model):
    if request.user.is_authenticated():
        data = model.objects.filter(author=request.user).order_by("-created_at")
        serializer = get_serializer(model, fields="__all__", rof=None)
        return serialize_many(data, serializer)
    return Response(status=status.HTTP_403_FORBIDDEN)


def get_bookmark(request, model):
    if request.user.is_authenticated():
        bookmarks = model.objects.filter(bookmark_user=request.user).order_by("-created_at")
        serializer = get_serializer(model, fields="__all__", rof=None)
        return serialize_many(bookmarks, serializer)
    return Response(status=status.HTTP_403_FORBIDDEN)