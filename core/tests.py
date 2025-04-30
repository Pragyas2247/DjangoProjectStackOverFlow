from django.test import TestCase

# Create your tests here.
from .models import User, Question

class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='pass')
        Question.objects.create(title='Test Question', body='Just a test', author=self.user, tags='django')

    def test_question_created(self):
        question = Question.objects.get(title='Test Question')
        self.assertEqual(question.author.username, 'testuser')
