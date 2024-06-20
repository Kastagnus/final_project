from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import resolve, Resolver404

# მომხმარებელი რომელიც მოხვდება მისმართზე 404 სტატუსით გადამისამართდება უახლოეს ხელმისაწვდომ ბმულზე
class Redirect404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, exception=None):
        response = self.get_response(request)
        if response.status_code == 404 and not request.path.startswith('/admin'):
            print(response.status_code)
            print('i am here 404')
            path = request.path
            while path and path != '/':
                try:
                    resolve(path)
                    break
                except Resolver404:
                    path = '/'.join(path.rstrip('/').split('/')[:-1]) + '/'
            return HttpResponseRedirect(path + '#')  # Redirect to a custom URL or anchor
        return response

# მომხმარებელი რომელიც გადამისამართდება შეზღუდული ინფორმაციის მისამართზე მიიღებს შესაბამის მესიჯს
class RedirectNotPermittedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, exception=None):
        response = self.get_response(request)
        if response.status_code == 403 and not request.path.startswith('/admin'):
            print(response.status_code)
            print('I am here')
            messages.info(request, 'You do not have access to this page.')
            return redirect('home')
        return response
