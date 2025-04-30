from rest_framework import viewsets, permissions, filters , generics, status
from .models import Question, Answer, Vote, User , Tag
from .serializers import QuestionSerializer, AnswerSerializer, VoteSerializer, UserSerializer, RegisterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] 

class QuestionFilter(django_filters.FilterSet): #Question filter based on title/Tags 
    title = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')

    class Meta:
        model = Question
        fields = ['title','tags']

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = QuestionFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'tags']
    
    def perform_create(self, serializer):
        # Automatically set the author as the logged-in user
        serializer.save(author=self.request.user)



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        answer = serializer.save(author=self.request.user)
        question_author = answer.question.author

        # Send email notification to question author
        if question_author.email:
            send_mail(
                subject='New Answer to Your Question',
                message=f'{self.request.user.username} answered your question: "{answer.question.title}"',
                from_email='no-reply@stackoverflow.com',
                recipient_list=[question_author.email],
                fail_silently=True,
            )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    

    def accept(self, request, pk=None):
        answer = self.get_object()
        
        if answer.question.author != request.user:
            return Response({'error': 'You are not the author of the question.'}, status=403)
        answer.is_accepted = True
        answer.save()

        # Send email notification to answer author
        if answer.author.email:
            send_mail(
                subject='Your Answer Was Accepted!',
                message=f'Your answer to "{answer.question.title}" was marked as accepted.',
                from_email='no-reply@stackoverflow.com',
                recipient_list=[answer.author.email],
                fail_silently=True,
            )

        return Response({'detail': 'Answer accepted successfully.'}, status=status.HTTP_200_OK)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
