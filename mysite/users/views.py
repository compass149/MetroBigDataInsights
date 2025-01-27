from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# 사용자 목록
@login_required(login_url='auth:login')
@permission_required('auth.view_user', raise_exception=True)
def get_users(request):
    page = request.GET.get('page', '1')
    searchType = request.GET.get('searchType', '').strip()
    searchKeyword = request.GET.get('searchKeyword', '').strip()

    # 사용자 목록 기본 쿼리
    users = User.objects.all().order_by('username')

    # 검색 필터 적용
    if searchType and searchKeyword:
        if searchType == 'all':
            users = users.filter(
                Q(username__icontains=searchKeyword) |
                Q(first_name__icontains=searchKeyword) |
                Q(email__icontains=searchKeyword)
            )
        elif searchType == 'username':
            users = users.filter(username__icontains=searchKeyword)
        elif searchType == 'first_name':
            users = users.filter(first_name__icontains=searchKeyword)
        elif searchType == 'email':
            users = users.filter(email__icontains=searchKeyword)

    # 페이지네이션 설정
    paginator = Paginator(users, 10)  # 페이지당 10명
    page_obj = paginator.get_page(page)

    # 순번 계산 (페이지 내 첫 번째 순번)
    start_index = paginator.per_page * (page_obj.number - 1)

    return render(request, 'users/list.html', {
        'users': page_obj,
        'searchType': searchType,
        'searchKeyword': searchKeyword,
        'start_index': start_index,  # 순번 계산용
    })


# 사용자 보기
@login_required(login_url='auth:login')
@permission_required('auth.view_user', raise_exception=True)
def get_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/read.html', {'user': user})


# 사용자 삭제
@login_required(login_url='auth:login')
@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, f"사용자 '{user.username}'이(가) 삭제되었습니다.")
    else:
        messages.error(request, "잘못된 요청입니다.")
    
    return HttpResponseRedirect(reverse('users:list'))
