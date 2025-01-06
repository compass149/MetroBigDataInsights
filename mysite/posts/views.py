#컨트롤러 역할  - request, response 담당
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .form import PostCreateForm
from .form2 import PostUpdateForm

#게시글 등록
# def create_post(request):
#     return HttpResponse('게시글 등록')
def create_post(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id = post.id)
        else:
            messages.error(request, '게시글 등록에 실패했습니다.')
    return render(request, 'posts/create.html', {'form': form})

#게시글 보기
#def get_post(request, post_id):
#    return HttpResponse('게시글 보기')
def get_post(request, post_id):
    post = get_object_or_404(Posts, id= post_id)
    return render(request, 'posts/read.html', {'post':post})

#게시글 수정
# def update_post(request, post_id):
#     return HttpResponse('게시글 수정')
def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    form = PostUpdateForm(instance=post)
    
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        
        if form.is_valid():
            if form.cleaned_data['password'] == post.password:
                post = form.save(commit=False)
                post.save()
                messages.success(request, '게시글이 수정되었습니다.')
                return redirect("posts:read", post_id = post.id)
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '게시글 수정에 실패했습니다.')
    return render(request, 'posts/update.html', {'form': form})
    
#게시글 삭제
#def delete_post(request, post_id):
#    return HttpResponse('게시글 삭제')
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    password = request.POST.get('password')
    
    if request.method == 'POST':
        if password == post.password:
            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
            return redirect('posts:list')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('posts:read', post_id = post.id)

#게시글 목록
# def get_posts(request):
#     return HttpResponse('게시글 목록')
def get_posts(request):
#    posts = Posts.objects.all().order_by('-created_at')
#    return render(request, 'posts/list.html', {'posts': posts})\
    page = request.GET.get('page', '1')
    posts = Posts.objects.all().order_by('-created_at')
    
    searchType = request.GET.get('searchType')
    searchKeyword = request.GET.get('searchKeyword')
    
    #검색 조건 처리
    if searchType not in [None, ''] and searchKeyword not in [None, '']:
        if searchType == 'all':
            posts = posts.filter(
                Q(title__contains=searchKeyword) |
                Q(content__contains=searchKeyword) |
                Q(username__contains=searchKeyword)
            )
        elif searchType == 'title':
            posts = posts.filter(
                Q(title__contains=searchKeyword)
            )
        elif searchType == 'content':
            posts = posts.filter(
                Q(content__contains=searchKeyword)
            )
        elif searchType == 'username':
            posts = posts.filter(
                Q(username__contains=searchKeyword)
            )
    
    #페이지네이션
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    
    # 현재 페이지의 첫 번째 게시글 번호 계산
    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))

    # 순번 계산하여 게시글 리스트에 추가
    for index, _ in enumerate(page_obj, start=0):
        page_obj[index].index_number = start_index - index

    #return render(request, 'posts/list.html', {'posts': page_obj})
    return render (request, 'posts/list.html', {
        'posts' : page_obj,
        'searchType':searchType,
        'searchKeyword' : searchKeyword
    })