from django.shortcuts import render, get_object_or_404, redirect    
from django.contrib.auth.decorators import login_required
from .models import Topic, Question, Answer
from users.models import User
from cuoora.retrievers import *

def topics_list_view(request):
    topics = Topic.objects.all()
    return render(request, "topics_list.html", {"topics": topics})

def question_details_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    context =  {'question': question, 'answers': answers}
    return render(request, 'question_details.html', context)

@login_required
def submit_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        desc = request.POST.get("description")
        if desc:
            Answer.objects.create(
                question=question,
                user=request.user,
                description=desc
            )
    return redirect("question_details", question_id=question.id)

def social_view(request):
    retriever = SocialQuestionRetriever(max_questions=10)
    user = request.user    
    questions = retriever.retrieve_sorted_questions(user)
    context = {"user": user, "questions": questions}
    return render(request, "social.html", context)

def topics_of_interest_view(request):
    retriever = TopicsQuestionRetriever(max_questions=10)
    user = request.user
    questions = retriever.retrieve_sorted_questions(user)
    context = {"user": user, "questions": questions}
    return render(request, "topics_of_interest.html", context)

def news_view(request):
    retriever = NewsQuestionRetriever(max_questions=10)
    user = request.user
    questions = retriever.retrieve_sorted_questions(user)
    context = {"user": user, "questions": questions}
    return render(request, "news.html", context)

def popular_today_view(request):
    retriever = PopularTodayQuestionRetriever(max_questions=10)
    user = request.user
    questions = retriever.retrieve_sorted_questions(user)
    context = {"user": user, "questions": questions}
    return render(request, "popular_today.html", context)
