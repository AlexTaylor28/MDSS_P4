from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

class Vote(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_positive_vote = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    votable = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return f"{self.is_positive_vote} by {self.user} on {self.votable}"

class Votable(models.Model):
    
    votes = GenericRelation('Vote')
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    class Meta:
        abstract = True
        
    def positive_votes(self):
        return self.votes.filter(is_positive_vote=True)

    def negative_votes(self):
        return self.votes.filter(is_positive_vote=False)

class QuestionManager(models.Manager):
    
    def published_today(self):
        today = timezone.now().date()
        return self.filter(timestamp__date=today)
    
    def popular_today(self):
        questions_published_today = self.published_today()

        questions_with_votes = [
            (question, question.positive_votes().count())
            for question in questions_published_today
        ]

        if not questions_with_votes:
            return self.none()

        total_positive_votes = sum(vote_count for _, vote_count in questions_with_votes)
        average_positive_votes = total_positive_votes / len(questions_with_votes)

        popular_question_ids = [
            question.id
            for question, vote_count in questions_with_votes
            if vote_count > average_positive_votes
        ]

        return self.filter(id__in=popular_question_ids)
        
class Question(Votable):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    topics = models.ManyToManyField('Topic', related_name='questions')
    title = models.CharField(max_length=255)
    
    objects = QuestionManager()
    
    def is_published_today():
        return self.timestamp == timezone.now().date()
    
    def __str__(self):
        return self.title
        
class Answer(Votable):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"{self.user.username} on '{self.question.title}': {self.description[:20]}"

class Topic(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name