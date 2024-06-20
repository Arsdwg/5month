from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'title description duration director reviews average_rating'.split()

    def get_average_rating(self, product):
        reviews = product.reviews.all()
        if reviews:
            sum_reviews = sum(i.stars for i in reviews)
            average = sum_reviews / len(reviews)
            return average
        return None


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    def get_movies_count(self, obj):
        return obj.movie_set.count()
    class Meta:
        model = models.Director
        fields = 'name movies_count'.split()

class DirectorsValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=100)


class ReviewsValidateSerializer(serializers.Serializer):
    stars_id = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()
    movie_id = serializers.IntegerField(min_value=1)

    def validate_movie_id(self, movie_id):
        try:
            models.Movie.objects.get(id=movie_id)
        except models.Movie.DoesNotExist:
            raise ValidationError('movie not found!')
        return movie_id

    def validate_stars_id(self, stars_id):
        try:
            models.Review.objects.get(id=stars_id)
        except models.Review.DoesNotExist:
            raise ValidationError('wrong number!')
        return stars_id


class MoviesValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=100)
    description = serializers.CharField()
    duration = serializers.IntegerField(min_value=1)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            models.Director.objects.get(id=director_id)
        except models.Director.DoesNotExist:
            raise ValidationError('director not found!')
        return director_id
