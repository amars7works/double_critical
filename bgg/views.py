from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Game
from registration.models import Profile
from rest_framework.decorators import api_view

class GameCorrection(APIView):

	def post(self, request, format="json"):
		response = Game.objects.create(**request.data)
		return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def user_auth_status(request, format="json"):
	username = request.data.get('username', None)
	profile_obj = Profile.objects.get(user__username=username)
	data =[]
	user = profile_obj.user
	if user.is_authenticated():
		return Response(user.is_authenticated,status=status.HTTP_200_OK)
	else:
		return Response(user.is_authenticated,status=status.HTTP_401_UNAUTHORIZED)