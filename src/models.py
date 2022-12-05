import requests, os

class GitHub:
    def __init__(self):
        self.client_id = os.environ.get('GITHUB_CLIENT_ID')
        self.client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
        self.scope = "read:user"
        self.allow_signup = "true"
        self.redirect_uri = "https://mexicodev.org"

    def login(self):
        client_id = self.client_id
        scope = self.scope
        allow_signup = self.allow_signup
        return f"https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}&allow_signup={allow_signup}"

    def auth(self, code):
        client_id = self.client_id
        client_secret = self.client_secret
        url = "https://github.com/login/oauth/access_token"
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        }
        headers = {
            'Accept': 'application/json'
        }
        resp = requests.post(url, data=data, headers=headers)
        return resp.json()
    
    def getData(self, token):
        url = "https://api.github.com/user"
        headers = {
            'Authorization': f"token {token}"
        }
        resp = requests.get(url, headers=headers)
        return resp.json()

