from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rauth import OAuth2Service
from rauth.utils import parse_utf8_qsl
import requests
from django.shortcuts import redirect


agiliq = OAuth2Service(
    client_id='121',
    client_secret='121',
    name='agiliq',
    authorize_url='http://10.42.0.04:8000/oauth/authorize',
    access_token_url='http://10.42.0.04:8000/oauth/access_token/',
    base_url='http://10.42.0.04:8000/')


def authorize(request):

    redirect_uri = 'http://127.0.0.1:8000/join/access_token'
    
    params = {'redirect_uri': redirect_uri,
            'response_type': 'code'}
    
    url = agiliq.get_authorize_url(**params)

    return  HttpResponseRedirect(url)



def get_access_token(request):
    authorize_code = request.GET['code']
    redirect_uri = 'http://127.0.0.1:8000/join/access_token'
    
    data = {'code': authorize_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        }
    
    response = agiliq.get_raw_access_token(data=data)
    
    json_data =  response.json()

    access_token = json_data['access_token']
    request.session['access_token'] = access_token

    return redirect(reverse('upload'))



def upload_resume(request):
    access_token = request.session.get('access_token','')
    resume = open('/home/uzhare/Desktop/howto-pyporting.pdf', 'rb')
    
    data = {    'first_name': 'Uzhare',
                'last_name': 'Farooq',
                'projects_url': 'https://github.com/uzhare',
                'code_url': 'https://github.com/warisamin/job.agiliq',
                }
    
    files = { 'resume' : ('resume.pdf', resume)}
    
    url = 'http://10.42.0.04:8000/api/resume/upload/?access_token=%s' % access_token
    final_post = requests.post(url, data=data, files = files)
    
    return HttpResponseRedirect('http://10.42.0.04:8000/accounts/profile')
