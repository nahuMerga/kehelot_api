from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Conversation, HeritageCard
from .serializers import UserSerializer, ConversationSerializer, HeritageCardSerializer
from .kehelot_service import  generate_ai_response


class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = User.objects.create_user(username=username, email=email, password=password)

        
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.pk 
        }, status=status.HTTP_201_CREATED)

class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

     
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):  
            refresh = RefreshToken.for_user(user) 
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.pk 
            })

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class AIChatView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        serializer = ConversationSerializer(data=request.data)

        if serializer.is_valid():
            user_input = serializer.validated_data['message']
            user = request.user 

           
            ai_response_in_amh = generate_ai_response(user_input)

           
            cache_key = f"chat_history_{user.id}"
            chat_history = cache.get(cache_key, [])

           
            chat_history.append({"user": user_input, "ai": ai_response_in_amh})
            cache.set(cache_key, chat_history, timeout=3600)  

           
            conversation = Conversation.objects.create(
                user=user,
                message=user_input,
                response=ai_response_in_amh
            )

            return Response({
                "message": "Conversation saved!",
                "conversation_id": conversation.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        conversations = Conversation.objects.filter(user=user).order_by('-timestamp')

        chat_data = []
        for conversation in conversations:
            chat_data.append({
                "history_id": conversation.id,
                "timestamp": conversation.timestamp.isoformat(),
                "messages": [
                    {"message": conversation.message, "response": conversation.response}
                ]
            })

        return Response({"user": user.username, "chat_history": chat_data})


class HeritageCardView(APIView):

    def get(self, request):
       
        cards = HeritageCard.objects.all()
        return Response(HeritageCardSerializer(cards, many=True).data)