from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ProfileUpdateForm

# 회원가입
# def register_account(request):
#     return HttpResponse ('회원가입')
def register_account(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                email=form.cleaned_data["email"]
            )
            user.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('auth:login')
        else:
            messages.error(request, '회원가입에 실패했습니다.')

    return render(request, 'accounts/register.html', {
        'form': form,
        'message_class': 'col-4 mx-auto'
    })


# 로그인
# def login_account(request):
#     return HttpResponse ('로그인')
# 로그인
def login_account(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # 로그인 실패
            if user is None:
                messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')
                return redirect('auth:login')

            # 로그인 성공
            login(request, user)
            return redirect('auth:profile')
        else:
            messages.error(request, '아이디 또는 비밀번호를 입력해주세요.')

    return render(request, 'accounts/login.html', {
        'form': form,
        'message_class': 'col-4 mx-auto'
    })

# def login_account(request):
#     return HttpResponse ('로그인')

# 로그아웃
# def logout_account(request):
#     return HttpResponse ('로그아웃')
def logout_account(request):
    logout(request)
    return redirect('auth:login')

# 프로필 보기
@login_required(login_url='auth:login')
def get_profile(request):
    return render(request, 'accounts/profile.html', {'message_class': 'col-4 mx-auto'})

#프로필 수정
@login_required(login_url='auth:login')
def update_account(request):
    form = ProfileUpdateForm(instance=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, '프로필 수정이 완료되었습니다.')
            return redirect('auth:profile')
        else:
            messages.error(request, '프로필 수정에 실패했습니다.')
            
    return render(request, 'accounts/update_profile.html',
                {'form': form, 'message_class': 'col-4 mx-auto'})
    
# 비밀번호 수정
def update_password(request):
    return HttpResponse ('비밀번호 수정')

# 아이디 찾기
def find_username(request):
    return HttpResponse ('아이디 찾기')

# 비밀번호 초기화
def reset_password(request):
    return HttpResponse ('비밀번호 초기화')

#사용자 탈퇴
def delete_account(request):
    return HttpResponse ('사용자 탈퇴')