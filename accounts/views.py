from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from rest_framework.permissions import IsAuthenticated 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(request):
    if request.method == 'PUT':
        user = request.user
        print(user)

        data = request.data

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        #user = authenticate(username=username, password=password)
        user = CustomUser.objects.get(username = username)

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)  
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Déconnecté avec succès.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









@api_view(['GET'])
def allBooks(request):
    books = Livre.objects.all()
    serialization = LivreSerializer(books, many=True)
    return Response(serialization.data)

@api_view(['GET']) 
def getbooks(request, id):
    book = Livre.objects.get(id = id)
    serializer = LivreSerializer(book)
    return Response(serializer.data)

@api_view(['POST'])
def addbooks(request):
    if request.method == 'POST':
        serializer = LivreSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérez l'utilisateur à ajouter en tant qu'auteur
            auteur_id = request.data.get('auteur')

            # Vérifiez le rôle de l'utilisateur à ajouter
            try:
                auteur = CustomUser.objects.get(id=auteur_id)
                if auteur.role == "auteur":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("Seuls les utilisateurs avec le rôle 'auteur' peuvent être ajoutés comme auteurs.", status=status.HTTP_403_FORBIDDEN)
            except CustomUser.DoesNotExist:
                return Response("L'utilisateur à ajouter en tant qu'auteur n'existe pas.", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def editbooks(request, id):
    book = Livre.objects.get(id = id)
    serialiser = LivreSerializer(instance = book, data = request.data)
    if serialiser.is_valid():
        serialiser.save()
    return Response(serialiser.data)


@api_view(['DELETE'])
def deletebooks(request, id):
    book = Livre.objects.get(id = id)
    book.delete()
    return Response("Livre supprimé avec succes!")