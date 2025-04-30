from rest_framework import serializers
from .models import User, Question, Answer, Vote

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    reputation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'reputation')
        
    #reputaion calculate the user's votes and accepted answer

    def get_reputation(self, user):
        # Votes on questions by the user
        question_votes = Vote.objects.filter(question__author=user)
        # Votes on answers by the user
        answer_votes = Vote.objects.filter(answer__author=user)
        # Accepted answers by the user
        accepted_answers = Answer.objects.filter(author=user, is_accepted=True)

        score = 0
        for vote in question_votes:
            score += 5 if vote.vote_type == 'up' else -2
        for vote in answer_votes:
            score += 10 if vote.vote_type == 'up' else -2
        score += accepted_answers.count() * 15
        return score

class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Question
        fields = 'id', 'title', 'body','tags', 'author','created_at'
        read_only_fields = 'author', 'created_at'
        
class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Answer
        fields = 'id', 'question', 'body', 'author', 'is_accepted', 'created_at'

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Vote
        fields = 'id', 'user', 'question', 'answer', 'vote_type'
