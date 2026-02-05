from django.contrib import admin
from .models import Quiz, Result


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'id', 'created_at')
    readonly_fields = ('id', 'created_at')
    search_fields = ('prompt', 'data')
    
    def get_title(self, obj):
        return obj.data.get('title', 'Untitled')
    get_title.short_description = 'Title'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_quiz_title', 'get_outcome', 'created_at')
    readonly_fields = ('id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    
    def get_quiz_title(self, obj):
        return obj.quiz.data.get('title', 'Untitled')
    get_quiz_title.short_description = 'Quiz'
    
    def get_outcome(self, obj):
        return obj.outcome.get('title', 'N/A')
    get_outcome.short_description = 'Outcome'
