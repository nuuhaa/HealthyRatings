from rest_framework import request, status, viewsets
from .models import Product, Rating
from .serializers import ProductSerializer, RatingSerializer, UserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            'token': token.key, 
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        response = {'message': 'You can’t create ratings like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Updated to reference Product
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def rate_product(self, request, pk=None):  # Updated method name and reference
        if 'stars' in request.data:
            product = Product.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                # Update rating if it exists
                rating = Rating.objects.get(user=user.id, product=product.id)  # Updated to reference Product
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating)
                json = {
                    'message': 'Product Rating Updated',
                    'result': serializer.data
                }
                return Response(json, status=status.HTTP_200_OK)

            except Rating.DoesNotExist:
                # Create a new rating if it doesn't exist
                rating = Rating.objects.create(stars=stars, product=product, user=user)  # Updated to reference Product
                serializer = RatingSerializer(rating)
                json = {
                    'message': 'Product Rating Created',
                    'result': serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)

        else:
            json = {
                'message': 'Stars not provided'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)