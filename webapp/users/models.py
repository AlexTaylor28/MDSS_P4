from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    topics_of_interest = models.ManyToManyField('cuoora.Topic', related_name='interested_users', blank=True)
    
    def __str__(self):
        return self.username

    def follow_user(self, user):
        if user != self:
            self.following.add(user)

    def unfollow_user(self, user):
        if user != self:
            self.following.remove(user)

    def follow_topic(self, topic):
        self.topics_of_interest.add(topic)

    def unfollow_topic(self, topic):
        self.topics_of_interest.remove(topic)
        
    def add_question(self, question):
        self.questions.add(question)

    def calculate_score(self):
        score = 0
        score += self._sum_votable_score(self.questions.all(), 10)
        score += self._sum_votable_score(self.answers.all(), 20)
        return score

    def _sum_votable_score(self, votables, points):
        return sum(points for v in votables if v.positive_votes().count() > v.negative_votes().count())

    def get_questions_from_following(self):
        from cuoora.models import Question
        return Question.objects.filter(user__in=self.following.all())
    
    def get_questions_from_topics_of_interest(self):
        from cuoora.models import Question
        return Question.objects.filter(topics__in=self.topics_of_interest.all()).exclude(user=self).distinct()