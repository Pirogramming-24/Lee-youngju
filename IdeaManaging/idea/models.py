from django.db import models
from tool.models import DevTool


class Idea(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='idea_images/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtools = models.ManyToManyField(DevTool, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def star_count(self):
        return self.ideastars.count()

    class Meta:
        ordering = ['-created_at']


class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='ideastars')
    user_identifier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'user_identifier')

    def __str__(self):
        return f'{self.user_identifier} - {self.idea.title}'
