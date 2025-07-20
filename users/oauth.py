import requests
import os
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from users.serializers import GoogleLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        code = serializer.validated_data['code']

        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data = {
                "code": code,
                "client_id": os.environ.get('GOOGLE_CLIENT_ID'),
                "client_secret": os.environ.get('GOOGLE_CLIENT_SECRET'),
                "redirect_uri": os.environ.get('GOOGLE_REDIRECT_URI'),
                "grant_type": "authorization_code",
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response ({"error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params = {"alt": "json"},
            headers = {"Authorization": f"Bearer {access_token}"}
        ).json()
        
        print(user_info)

        email = user_info["email"]
        # given_name = user_info["given_name"]
        # family_name = user_info["family_name"]
        # picture = user_info["picture"]

        user, created = User.objects.get_or_create(
            email = email,
            defaults={
                "first_name": user_info["given_name"],
                "last_name": user_info["family_name"],
                "avatar": user_info["picture"],
            }
        )

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email

        return Response({"access_token": str(refresh.access_token), "refresh_token": str(refresh)})
