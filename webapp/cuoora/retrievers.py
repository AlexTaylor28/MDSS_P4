from django.db.models import Count, Q
from abc import ABC, abstractmethod
from django.utils import timezone
from cuoora.models import Question, Vote, User

class QuestionRetriever(ABC):
    
    def __init__(self, max_questions):
        self.max_questions = max_questions

    def retrieve_sorted_questions(self, user):
        questions = self.retrieve_questions(user)
        questions = questions.annotate(positive_votes_count=Count('votes', filter=Q(votes__is_positive_vote=True)))
        questions = questions.order_by('-positive_votes_count')
        return questions[:self.max_questions]
            
    @abstractmethod
    def retrieve_questions(self, user):
        pass

class SocialQuestionRetriever(QuestionRetriever):
    
    def retrieve_questions(self, user):
        return user.get_questions_from_following()

class TopicsQuestionRetriever(QuestionRetriever):
    
    def retrieve_questions(self, user):
        return user.get_questions_from_topics_of_interest()

class NewsQuestionRetriever(QuestionRetriever):
    
    def retrieve_questions(self, user):
        return Question.objects.published_today()

class PopularTodayQuestionRetriever(QuestionRetriever):
    
    def retrieve_questions(self, user):
        return Question.objects.popular_today()