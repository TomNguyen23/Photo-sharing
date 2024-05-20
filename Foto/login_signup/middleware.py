from django.http import HttpResponseRedirect
from django.shortcuts import render
from foto_crud.models import User

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path in ['/login', '/signup', '/logout', '/login/', '/signup/', '/logout/', '/', '/home/', '/home']:
            response = self.get_response(request)
            return response
        
        cookie_name = 'cookie'
        if cookie_name not in request.COOKIES:
            # redirect to login page
            response = HttpResponseRedirect('/login')
            return response
        cookie = request.COOKIES[cookie_name]
        user = User.objects.filter(cookies=cookie).first()
        if not user:
            reponse = HttpResponseRedirect('/login')
            return response
        request.user = user
        response = self.get_response(request)
        return response
