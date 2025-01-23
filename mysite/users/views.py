from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

# 사용자 목록
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    page = request.GET.get('page', '1')
    searchType = request.GET.get('searchType')
    searchKeyword = request.GET.get('searchKeyword')
    users = User.objects.all().order_by('username')

    # 검색 조건 처리
    if searchType not in [None, ''] and searchKeyword not in [None, '']:
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

    # 페이지네이션
    paginator = Paginator(users, 10)  # 페이지당 10명
    page_obj = paginator.get_page(page)

    # 사용자 리스트에 순번 추가
    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))
    users_with_index = [
        {
            'index_num': start_index - idx,
            'user': user
        }
        for idx, user in enumerate(page_obj)
    ]

    return render(request, 'users/list.html', {
        'users': users_with_index,
        'searchType': searchType,
        'searchKeyword': searchKeyword,
        'paginator': paginator,
        'page_obj': page_obj,
    })


# 사용자 보기
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def get_user(request, user_id):
    return HttpResponse('사용자 보기')


# 사용자 삭제
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    return HttpResponse('사용자 삭제')
