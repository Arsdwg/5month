from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, MoviesValidateSerializer, ReviewsValidateSerializer, DirectorsValidateSerializer
from .models import Director, Movie, Review
from django.db.models import Avg

# Create your views here.
@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        data = Director.objects.all()
        list_ = DirectorSerializer(data, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        serializer = DirectorsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        name = serializer.validated_data.get('name')
        director = Director.objects.create(
            name=name
        )
        return Response(data={'director_id': director.id, 'name': director.name}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail(request, id):
    try:
        product = Director.objects.get(id=id)

    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        product.name = serializer.validated_data.get('name')
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        data = Movie.objects.all()
        list_ = MovieSerializer(data, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        serializer = MoviesValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id
        )
        return Response(data={'movie_id': movie.id, 'title': movie.title, 'description': movie.description,
                              'duration': movie.duration, 'director_id': movie.director_id},
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, id):
    try:
        product = Movie.objects.get(id=id)

    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MoviesValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.duration = serializer.validated_data.get('duration')
        product.director_id = serializer.validated_data.get('director_id')

        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        data = Review.objects.all()
        list_ = ReviewSerializer(data, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        serializer = ReviewsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        stars_id = serializer.validated_data.get('stars_id')
        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id')

        review = Review.objects.create(
            stars_id=stars_id,
            text=text,
            movie_id=movie_id
        )
        return Response(data={'stars_id': review.stars_id, 'text': review.text, 'movie_id': review.movie_id},
                        status=status.HTTP_201_CREATED)


def calculate_average_rating():
    return Review.objects.aggregate(Avg('stars'))['stars__avg']


@api_view(['GET'])
def review_detail(request, id):
    try:
        product = Review.objects.get(id=id)

    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    average_rating = calculate_average_rating()
    if request.method == 'GET':
        data = ReviewSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

        product.stars_id = serializer.validated_data.get('stars_id')
        product.text = serializer.validated_data.get('text')
        product.movie_id = serializer.validated_data.get('movie_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
