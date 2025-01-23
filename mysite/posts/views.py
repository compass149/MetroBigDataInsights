import os
import uuid
from urllib.parse import quote
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from mysite import settings
from .models import Posts
from .form import PostCreateForm
from .form2 import PostUpdateForm
from comments.models import Comments

# 공통 함수: 파일 저장 경로 처리
def get_file_path(post_id, filename):
    return os.path.join(settings.MEDIA_ROOT, 'posts', str(post_id), filename)

def save_file(file, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# 게시글 등록
@login_required(login_url='auth:login')
def create_post(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.updated_by = request.user
            post.save()

            # 파일 업로드 처리
            file = request.FILES.get('uploadFile')
            if file:
                filename = uuid.uuid4().hex
                file_path = get_file_path(post.id, filename)
                save_file(file, file_path)
                post.filename = filename
                post.original_filename = file.name
                post.save()

            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, '게시글 등록에 실패했습니다.')
    return render(request, 'posts/create.html', {'form': form})

# 게시글 보기
@login_required(login_url='auth:login')
def get_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    comments = Comments.objects.filter(post=post).order_by('-created_at')
    return render(request, 'posts/read.html', {'post': post, 'comments': comments})

# 게시글 수정
@login_required(login_url='auth:login')
def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    if post.created_by != request.user:
        messages.error(request, '게시글 수정 권한이 없습니다.')
        return redirect('posts:read', post_id=post.id)

    form = PostUpdateForm(instance=post)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.updated_by = request.user

            # 파일 삭제 처리
            if form.cleaned_data.get('deleteFile') and post.filename:
                delete_file(get_file_path(post.id, post.filename))
                post.filename = None
                post.original_filename = None

            # 새 파일 업로드 처리
            new_file = request.FILES.get('uploadFile')
            if new_file:
                if post.filename:
                    delete_file(get_file_path(post.id, post.filename))
                filename = uuid.uuid4().hex
                file_path = get_file_path(post.id, filename)
                save_file(new_file, file_path)
                post.filename = filename
                post.original_filename = new_file.name

            post.save()
            messages.success(request, '게시글이 수정되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, '게시글 수정에 실패했습니다.')

    return render(request, 'posts/update.html', {'form': form, 'post': post})

# 게시글 삭제
@login_required(login_url='auth:login')
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    if post.created_by != request.user:
        messages.error(request, '게시글 삭제 권한이 없습니다.')
        return redirect('posts:read', post_id=post.id)

    if request.method == 'POST':
        if post.filename:
            delete_file(get_file_path(post.id, post.filename))
        post.delete()
        messages.success(request, '게시글이 삭제되었습니다.')
        return redirect('posts:list')

# 게시글 목록
@login_required(login_url='auth:login')
def get_posts(request):
    page = request.GET.get('page', '1')
    search_type = request.GET.get('searchType')
    search_keyword = request.GET.get('searchKeyword')
    posts = Posts.objects.all().order_by('-created_at')

    # 검색 처리
    if search_type and search_keyword:
        filters = {
            'all': Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword),
            'title': Q(title__icontains=search_keyword),
            'content': Q(content__icontains=search_keyword),
            'full_name': Q(created_by__first_name__icontains=search_keyword),
        }
        posts = posts.filter(filters.get(search_type, Q()))

    # 페이지네이션
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    # 순번 추가
    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))
    for idx, post in enumerate(page_obj, start=0):
        post.index_number = start_index - idx

    return render(request, 'posts/list.html', {
        'posts': page_obj,
        'searchType': search_type,
        'searchKeyword': search_keyword,
    })

# 첨부파일 다운로드
def download_file(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    file_path = get_file_path(post.id, post.filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            encoded_filename = quote(post.original_filename)
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            return response
    return HttpResponse(status=404)
