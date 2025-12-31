from django.shortcuts import render, get_object_or_404, redirect
from .models import Review

# Create your views here.

def review_list(request):
    """리뷰 리스트 페이지 - 정렬 기능 포함"""
    sort_by = request.GET.get('sort', '-created_at')

    # 정렬 옵션 검증
    valid_sort_options = ['title', '-title', 'rating', '-rating', 'runtime', '-runtime', 'release_year', '-release_year']
    if sort_by not in valid_sort_options:
        sort_by = '-created_at'

    reviews = Review.objects.all().order_by(sort_by)

    context = {
        'reviews': reviews,
        'current_sort': sort_by,
    }
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, pk):
    """리뷰 디테일 페이지"""
    review = get_object_or_404(Review, pk=pk)
    context = {
        'review': review,
    }
    return render(request, 'reviews/review_detail.html', context)


def review_create(request):
    """리뷰 작성 페이지"""
    if request.method == 'POST':
        review = Review(
            title=request.POST.get('title'),
            director=request.POST.get('director'),
            actors=request.POST.get('actors'),
            genre=request.POST.get('genre'),
            rating=request.POST.get('rating'),
            runtime=request.POST.get('runtime'),
            release_year=request.POST.get('release_year'),
            content=request.POST.get('content'),
        )
        review.save()
        return redirect('review_list')

    context = {
        'genre_choices': Review.GENRE_CHOICES,
        'rating_choices': Review.RATING_CHOICES,
    }
    return render(request, 'reviews/review_form.html', context)


def review_update(request, pk):
    """리뷰 수정 페이지"""
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.actors = request.POST.get('actors')
        review.genre = request.POST.get('genre')
        review.rating = request.POST.get('rating')
        review.runtime = request.POST.get('runtime')
        review.release_year = request.POST.get('release_year')
        review.content = request.POST.get('content')
        review.save()
        return redirect('review_detail', pk=review.pk)

    context = {
        'review': review,
        'genre_choices': Review.GENRE_CHOICES,
        'rating_choices': Review.RATING_CHOICES,
        'is_update': True,
    }
    return render(request, 'reviews/review_form.html', context)


def review_delete(request, pk):
    """리뷰 삭제"""
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return redirect('review_detail', pk=pk)
