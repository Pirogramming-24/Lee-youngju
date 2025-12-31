from django.db import models

# Create your models here.


class Review(models.Model):
    GENRE_CHOICES = [
        ("액션", "액션"),
        ("코미디", "코미디"),
        ("드라마", "드라마"),
        ("스릴러", "스릴러"),
        ("공포", "공포"),
        ("로맨스", "로맨스"),
        ("SF", "SF"),
        ("판타지", "판타지"),
        ("애니메이션", "애니메이션"),
        ("다큐멘터리", "다큐멘터리"),
    ]

    RATING_CHOICES = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]

    title = models.CharField(max_length=200, verbose_name="영화 제목")
    director = models.CharField(max_length=100, verbose_name="감독")
    actors = models.CharField(max_length=200, verbose_name="주연")
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name="장르")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="별점")
    runtime = models.IntegerField(verbose_name="러닝타임(분)")
    release_year = models.IntegerField(verbose_name="개봉 연도")
    content = models.TextField(verbose_name="리뷰 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.title

    def get_runtime_display(self):
        """러닝타임  몇시간 몇분 형식으로 반환"""
        hours = self.runtime // 60
        minutes = self.runtime % 60
        return f"{hours}시간 {minutes}분"

    class Meta:
        verbose_name = "영화 리뷰"
        verbose_name_plural = "영화 리뷰들"
        ordering = ["-created_at"]
