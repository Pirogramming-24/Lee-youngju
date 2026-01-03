from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from .models import Idea, IdeaStar
from tool.models import DevTool


def get_user_identifier(request):
    """세션에서 사용자 식별자를 가져오거나 생성"""
    if 'user_id' not in request.session:
        import uuid
        request.session['user_id'] = str(uuid.uuid4())
    return request.session['user_id']


def idea_list(request):
    """아이디어 리스트 페이지 (메인 페이지)"""
    ideas = Idea.objects.annotate(star_count=Count('ideastars')).prefetch_related('devtools').all()

    # 정렬 기능
    sort = request.GET.get('sort', 'latest')
    if sort == 'star':
        ideas = ideas.order_by('-star_count', '-created_at')
    elif sort == 'name':
        ideas = ideas.order_by('title')
    elif sort == 'oldest':
        ideas = ideas.order_by('created_at')
    else:  # latest (기본값)
        ideas = ideas.order_by('-created_at')

    # 페이지네이션 (한 페이지에 4개씩)
    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 사용자 식별자 가져오기
    user_id = get_user_identifier(request)

    # 각 아이디어에 대한 찜 여부 추가
    for idea in page_obj:
        idea.is_starred = IdeaStar.objects.filter(idea=idea, user_identifier=user_id).exists()

    context = {
        'page_obj': page_obj,
        'current_sort': sort,
    }
    return render(request, 'idea/idea_list.html', context)


def idea_detail(request, idea_id):
    """아이디어 상세 페이지"""
    idea = get_object_or_404(Idea, pk=idea_id)
    user_id = get_user_identifier(request)
    is_starred = IdeaStar.objects.filter(idea=idea, user_identifier=user_id).exists()

    context = {
        'idea': idea,
        'is_starred': is_starred,
    }
    return render(request, 'idea/idea_detail.html', context)


def idea_register(request):
    """아이디어 등록 페이지"""
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        interest = request.POST.get('interest', 0)
        devtool_ids = request.POST.getlist('devtools')  # 여러 개 선택

        idea = Idea.objects.create(
            title=title,
            image=image,
            content=content,
            interest=interest
        )

        # ManyToMany 관계 설정
        idea.devtools.set(devtool_ids)

        return redirect('idea:detail', idea_id=idea.id)

    devtools = DevTool.objects.all()
    context = {'devtools': devtools}
    return render(request, 'idea/idea_register.html', context)


def idea_update(request, idea_id):
    """아이디어 수정 페이지"""
    idea = get_object_or_404(Idea, pk=idea_id)

    if request.method == 'POST':
        idea.title = request.POST.get('title')
        if request.FILES.get('image'):
            idea.image = request.FILES.get('image')
        idea.content = request.POST.get('content')
        idea.interest = request.POST.get('interest')
        devtool_ids = request.POST.getlist('devtools')  # 여러 개 선택
        idea.save()

        # ManyToMany 관계 업데이트
        idea.devtools.set(devtool_ids)

        return redirect('idea:detail', idea_id=idea.id)

    devtools = DevTool.objects.all()
    context = {
        'idea': idea,
        'devtools': devtools,
    }
    return render(request, 'idea/idea_update.html', context)


def idea_delete(request, idea_id):
    """아이디어 삭제"""
    idea = get_object_or_404(Idea, pk=idea_id)
    if request.method == 'POST':
        idea.delete()
        return redirect('idea:list')
    return redirect('idea:detail', idea_id=idea_id)


def toggle_star(request, idea_id):
    """찜하기 토글 (AJAX)"""
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=idea_id)
        user_id = get_user_identifier(request)

        star = IdeaStar.objects.filter(idea=idea, user_identifier=user_id).first()

        if star:
            star.delete()
            is_starred = False
        else:
            IdeaStar.objects.create(idea=idea, user_identifier=user_id)
            is_starred = True

        star_count = idea.star_count()

        return JsonResponse({
            'is_starred': is_starred,
            'star_count': star_count
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


def adjust_interest(request, idea_id):
    """관심도 조절 (AJAX)"""
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=idea_id)
        action = request.POST.get('action')

        if action == 'increase':
            idea.interest += 1
        elif action == 'decrease':
            idea.interest = max(0, idea.interest - 1)

        idea.save()

        return JsonResponse({
            'interest': idea.interest
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
