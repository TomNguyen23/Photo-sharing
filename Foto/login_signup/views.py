import hashlib
from django.http import HttpResponseRedirect
from django.shortcuts import render
from foto_crud.models import User

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username).first()

        hashed_password = hash_password(password)

        if user is None:
            return render(request, 'login_signup/login.html', {'error': 'Không tìm thấy người dùng'})
        if user.password != hashed_password:
            return render(request, 'login_signup/login.html', {'error': 'Sai mật khẩu'})
        
        response = HttpResponseRedirect('/')
        response.set_cookie('cookie', user.cookies)
        return response
    else:
        return render(request, 'login_signup/login.html')
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not valid(password):
            return render(request, 'login_signup/signup.html', {'error': 'Mật khẩu phải chứa ít nhất 8 ký tự, 1 chữ hoa, 1 chữ thường và 1 số'})

        user = User.objects.get(username=username).first()
        
        if user is not None:
            return render(request, 'login_signup/signup.html', {'error': 'Tên người dùng đã tồn tại'})
        
        hashed_password = hash_password(password)
        cookies = hash_password(username + password)
        user = User(username=username, password=hashed_password, cookies=cookies)
        user.save()
        
        response = HttpResponseRedirect('/')
        response.set_cookie('cookie', cookies)
        return response
    else:
        return render(request, 'login_signup/signup.html')
    
def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cookie')
    return response

def hash_password(password):
    password = password.encode('utf-8')
    hashing = hashlib.md5()
    hashing = hashing.update(password.encode())
    return hashing.hexdigest()
        
def valid(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    return True