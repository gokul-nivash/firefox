import requests
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
# Create your views here.
from rest_framework.response import Response

from firefox.settings import env


def login(request):
  return render(request, 'login.html')

@login_required
def home(request):
  return render(request, 'home.html')

class GetFaceBookPageDetailsView(generics.GenericAPIView):
  def get(self,request):
    try:
      # GET Access Token
      client_id = env('SOCIAL_AUTH_FACEBOOK_KEY')
      client_secret = env('SOCIAL_AUTH_FACEBOOK_SECRET')
      exchange_token = env('EXCHANGE_TOKEN')
      user_id = env('USER_ID')

      access_token_url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(client_id,client_secret,exchange_token)
      access_token_api_call = requests.get(access_token_url)
      access_token_result = access_token_api_call.json()
      print(access_token_result)
      if access_token_result.get('access_token'):
        access_token = access_token_result['access_token']

      # GET FaceBook Page Data

        facebook_data_pages_url = 'https://graph.facebook.com/{}/accounts?fields=name,access_token&access_token={}'.format(user_id,access_token)
        facebook_data_pages_api_call = requests.get(facebook_data_pages_url)
        facebook_data_pages_result = facebook_data_pages_api_call.json()
        print(facebook_data_pages_result)
      else:
        return Response({'message':'Exchange Token Expired'})
      return Response({"status": "success", "message": "Face Book Page Details", 'data': facebook_data_pages_result})

    except Exception as e:
      print('Exception {}'.format(e.args))
      return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PageTemplateView(generics.GenericAPIView):
  def get(self, request):
    try:
      return render(request, 'facebook_pages.html')
    except Exception as e:
      print('Exception {}'.format(e.args))
      return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
