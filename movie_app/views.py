from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from .models import Director, Movie, Review


# Create your views here.
@api_view(['GET'])
def director_list_api_view(request):
    data = Director.objects.all()

    list_ = DirectorSerializer(data, many=True).data


    return Response(data=list_)

@api_view(['GET'])
def director_detail(request, id):
    try:
        product = Director.objects.get(id=id)

    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = DirectorSerializer(product).data

    return Response(data=data)


@api_view(['GET'])
def movie_list_api_view(request):
    data = Movie.objects.all()

    list_ = MovieSerializer(data, many=True).data


    return Response(data=list_)

@api_view(['GET'])
def movie_detail(request, id):
    try:
        product = Movie.objects.get(id=id)

    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = MovieSerializer(product).data

    return Response(data=data)



@api_view(['GET'])
def review_list_api_view(request):
    data = Review.objects.all()

    list_ = ReviewSerializer(data, many=True).data


    return Response(data=list_)

@api_view(['GET'])
def review_detail(request, id):
    try:
        product = Review.objects.get(id=id)

    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = ReviewSerializer(product).data

    return Response(data=data)
