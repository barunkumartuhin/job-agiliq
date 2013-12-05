from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rauth import OAuth2Service
from rauth.utils import parse_utf8_qsl
import requests
from django.shortcuts import redirect


agiliq = OAuth2Service(
    client_id='<my_client_id>',
    client_secret='<my_client_secret>',
    name='agiliq',
    authorize_url='http://join.agiliq.com/oauth/authorize/',
    access_token_url='http://join.agiliq.com/oauth/access_token/',
    base_url='http://join.agiliq.com/')


# View to authorize app
def authorize(request):

    redirect_uri = 'http://127.0.0.1:8000/join/access_token'
    params = {'redirect_uri': redirect_uri,
            'response_type': 'code'}
    
    url = agiliq.get_authorize_url(**params)

    return  HttpResponseRedirect(url)


# View to get access token
def get_access_token(request):
    # Authorization code from authorize view
    authorize_code = request.GET['code']
    redirect_uri = 'http://127.0.0.1:8000/join/access_token'
    
    data = {'code': authorize_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        }
    
    response = agiliq.get_raw_access_token(data=data)
    # We have raw access token in response
    json_data =  response.json()
    # Retreive access token from json data.
    access_token = json_data['access_token']
    request.session['access_token'] = access_token

    return redirect(reverse('upload'))


# View to upload resume and personal infromation.
def upload_resume(request):
    access_token = request.session.get('access_token','')
    resume = open('<path_to_my_resume>', 'rb')
    
    data = {    'first_name': 'Uzhare',
                'last_name': 'Farooq',
                'projects_url': 'https://github.com/uzhare',
                'code_url': 'https://github.com/uzhare/job-agiliq',
                }
    
    files = { 'resume' : ('uzhare_resume.pdf', resume)}
    
    url = 'http://join.agiliq.com/api/resume/upload/?access_token=%s' % access_token
    final_post = requests.post(url, data=data, files = files)
    
    return HttpResponseRedirect('http://join.agiliq.com/accounts/profile')
