import uuid
from django.db import models


class Quiz(models.Model):
    """A quiz - generated from a single prompt, stored as JSON"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.TextField(help_text="The original prompt used to generate this quiz")
    data = models.JSONField(help_text="The quiz content: title, questions, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "quizzes"
    
    def __str__(self):
        return f"{self.data.get('title', 'Untitled Quiz')} ({self.id})"


class Result(models.Model):
    """A quiz result - someone's answers and their outcome"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    name = models.CharField(max_length=200, blank=True, help_text="Taker's name (optional)")
    answers = models.JSONField(help_text="Their answers as a JSON blob")
    outcome = models.JSONField(help_text="The result they got")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        name = self.name or "Anonymous"
        return f"{name} - {self.quiz.data.get('title', 'Quiz')} ({self.id})"
