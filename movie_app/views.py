from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
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
        name = request.data.get('name')
        director = Director.objects.create(
            name=name,
        )
        director.save()
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
        product.name = request.data.get('name')
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
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id,
        )
        movie.save()
        return Response(data={'movie_id': movie.id, 'title': movie.title, 'description': movie.description,
                              'duration': movie.duration, 'director_id': movie.director_id}, status=status.HTTP_201_CREATED)

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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.duration = request.data.get('duration')
        product.director_id = request.data.get('director_id')
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
        stars = request.data.get('stars')
        descript = request.data.get('descript')
        movie_id = request.data.get('movie_id')
        review = Review.objects.create(
            stars=stars,
            descript=descript,
            movie_id=movie_id,
        )
        review.save()
        return Response(data={'review_id': review.id, 'movie': review.movie_id}, status=status.HTTP_201_CREATED)


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
        product.stars = request.data.get('stars')
        product.descript = request.data.get('descript')
        product.movie_id = request.data.get('movie_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
