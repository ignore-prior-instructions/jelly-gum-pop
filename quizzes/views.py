from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Quiz, Result
from .llm import generate_quiz, regenerate_quiz


def home(request):
    """Landing page - prompt goes in, quiz comes out"""
    return render(request, 'quizzes/home.html')


@require_http_methods(["POST"])
def create_quiz(request):
    """Generate a quiz from a prompt"""
    prompt = request.POST.get('prompt', '').strip()
    
    if not prompt:
        return JsonResponse({'error': 'Prompt required'}, status=400)
    
    try:
        # Generate the quiz
        quiz_data = generate_quiz(prompt)
        
        # Save it
        quiz = Quiz.objects.create(
            prompt=prompt,
            data=quiz_data
        )
        
        # Redirect to the quiz page
        return redirect('take_quiz', quiz_id=quiz.id)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def take_quiz(request, quiz_id):
    """Show a quiz for taking"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quizzes/take.html', {'quiz': quiz})


@require_http_methods(["POST"])
def submit_quiz(request, quiz_id):
    """Submit quiz answers and get result"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Collect answers
    answers = []
    for i, question in enumerate(quiz.data['questions']):
        answer_key = f'question_{i}'
        answer_index = request.POST.get(answer_key)
        
        if answer_index is not None:
            answer_index = int(answer_index)
            answers.append({
                'question_index': i,
                'answer_index': answer_index,
                'answer_text': question['options'][answer_index]['text'],
                'points': question['options'][answer_index].get('points', 0)
            })
    
    # Calculate score
    total_score = sum(a['points'] for a in answers)
    
    # Find matching outcome
    outcome = None
    for possible_outcome in quiz.data['outcomes']:
        min_score = possible_outcome.get('min_score', 0)
        max_score = possible_outcome.get('max_score', 999)
        
        if min_score <= total_score <= max_score:
            outcome = possible_outcome
            break
    
    # Default outcome if none matched
    if not outcome:
        outcome = quiz.data['outcomes'][0]
    
    # Save result
    name = request.POST.get('name', '').strip()
    result = Result.objects.create(
        quiz=quiz,
        name=name,
        answers=answers,
        outcome=outcome
    )
    
    return redirect('view_result', result_id=result.id)


def view_result(request, result_id):
    """Show quiz result - the shareable page"""
    result = get_object_or_404(Result, id=result_id)
    return render(request, 'quizzes/result.html', {'result': result})


@require_http_methods(["POST"])
def nudge_quiz(request, quiz_id):
    """Regenerate a quiz with a nudge"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    nudge = request.POST.get('nudge', '').strip()
    
    if not nudge:
        return JsonResponse({'error': 'Nudge required'}, status=400)
    
    try:
        # Regenerate with nudge
        new_data = regenerate_quiz(quiz.prompt, nudge, quiz.data)
        
        # Update the quiz
        quiz.data = new_data
        quiz.save()
        
        return redirect('take_quiz', quiz_id=quiz.id)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
