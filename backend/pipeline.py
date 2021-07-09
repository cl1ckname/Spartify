import datetime

def save_access_token(backend, user, response, details, is_new=False,*args,**kwargs):
    if backend.name=='spotify':
        print('-----------')
        print(user.oauth_token)
        print(response)
        print('-----------')
        user.oauth_token = response['access_token']
        user.refresh_token = response['refresh_token']
        user.expires = datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])
        user.save()
        