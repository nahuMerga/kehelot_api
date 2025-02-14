from django.urls import path
from .views import RegisterUserView, LoginUserView, AIChatView, HeritageCardView, ChatHistoryView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginUserView.as_view()),
    path("chat/", AIChatView.as_view()),
    path("heritage/", HeritageCardView.as_view()),
    path('chat_history/', ChatHistoryView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access & refresh token
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token

]
