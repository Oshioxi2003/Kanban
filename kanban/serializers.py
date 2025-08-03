from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import (
    Board, List, Card, Comment, UserProfile, Label, CardActivity, Goal, 
    Notification, TaskChecklist, PomodoroSession, Team, TeamMembership
)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'display_name', 'bio']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with profile"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile', 'full_name']
    
    def get_full_name(self, obj):
        return obj.profile.name if hasattr(obj, 'profile') else obj.username


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    display_name = serializers.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'display_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        display_name = validated_data.pop('display_name', None)
        
        user = User.objects.create_user(**validated_data)
        
        if display_name:
            user.profile.display_name = display_name
            user.profile.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for Label model"""
    class Meta:
        model = Label
        fields = ['id', 'name', 'color', 'created_at']
        read_only_fields = ['created_at']


class CardActivitySerializer(serializers.ModelSerializer):
    """Serializer for CardActivity model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CardActivity
        fields = ['id', 'activity_type', 'description', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CardSerializer(serializers.ModelSerializer):
    """Serializer for Card model"""
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    labels = LabelSerializer(many=True, read_only=True)
    label_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    comments = CommentSerializer(many=True, read_only=True)
    activities = CardActivitySerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    is_due_soon = serializers.ReadOnlyField()
    
    class Meta:
        model = Card
        fields = [
            'id', 'title', 'description', 'assignee', 'assignee_id', 
            'labels', 'label_ids', 'priority', 'position', 'due_date', 
            'estimated_hours', 'created_at', 'updated_at', 'completed', 
            'completed_at', 'comments', 'activities', 'is_overdue', 'is_due_soon'
        ]
        read_only_fields = ['created_at', 'updated_at', 'completed_at']
    
    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        label_ids = validated_data.pop('label_ids', [])
        
        card = Card.objects.create(**validated_data)
        
        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                card.assignee = assignee
                card.save()
            except User.DoesNotExist:
                pass
        
        if label_ids:
            labels = Label.objects.filter(id__in=label_ids, user=self.context['request'].user)
            card.labels.set(labels)
        
        # Create activity
        CardActivity.objects.create(
            card=card,
            user=self.context['request'].user,
            activity_type='created',
            description=f"Created card '{card.title}'"
        )
        
        return card
    
    def update(self, instance, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        label_ids = validated_data.pop('label_ids', None)
        
        old_values = {
            'title': instance.title,
            'assignee': instance.assignee,
            'completed': instance.completed
        }
        
        if assignee_id is not None:
            try:
                assignee = User.objects.get(id=assignee_id) if assignee_id else None
                instance.assignee = assignee
            except User.DoesNotExist:
                pass
        
        if label_ids is not None:
            labels = Label.objects.filter(id__in=label_ids, user=self.context['request'].user)
            instance.labels.set(labels)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Create activities for significant changes
        user = self.context['request'].user
        
        if old_values['title'] != instance.title:
            CardActivity.objects.create(
                card=instance,
                user=user,
                activity_type='updated',
                description=f"Changed title from '{old_values['title']}' to '{instance.title}'"
            )
        
        if old_values['assignee'] != instance.assignee:
            if instance.assignee:
                CardActivity.objects.create(
                    card=instance,
                    user=user,
                    activity_type='assigned',
                    description=f"Assigned to {instance.assignee.profile.name}"
                )
            else:
                CardActivity.objects.create(
                    card=instance,
                    user=user,
                    activity_type='updated',
                    description="Removed assignee"
                )
        
        if not old_values['completed'] and instance.completed:
            CardActivity.objects.create(
                card=instance,
                user=user,
                activity_type='completed',
                description=f"Marked card as completed"
            )
        
        return instance


class ListSerializer(serializers.ModelSerializer):
    """Serializer for List model"""
    cards = CardSerializer(many=True, read_only=True)
    cards_count = serializers.SerializerMethodField()
    
    class Meta:
        model = List
        fields = ['id', 'title', 'position', 'created_at', 'updated_at', 'cards', 'cards_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_cards_count(self, obj):
        return obj.cards.count()


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for Board model"""
    owner = UserSerializer(read_only=True)
    lists = ListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = [
            'id', 'title', 'description', 'owner', 'created_at', 
            'updated_at', 'is_active', 'is_template', 'lists'
        ]
        read_only_fields = ['created_at', 'updated_at']


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for Goal model"""
    owner = UserSerializer(read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    cards_count = serializers.SerializerMethodField()
    completed_cards_count = serializers.SerializerMethodField()
    cards = CardSerializer(many=True, read_only=True)
    
    class Meta:
        model = Goal
        fields = [
            'id', 'title', 'description', 'owner', 'target_date', 
            'is_completed', 'completed_at', 'created_at', 'updated_at',
            'progress_percentage', 'is_overdue', 'cards_count', 
            'completed_cards_count', 'cards'
        ]
        read_only_fields = ['created_at', 'updated_at', 'completed_at']
    
    def get_cards_count(self, obj):
        return obj.cards.count()
    
    def get_completed_cards_count(self, obj):
        return obj.cards.filter(completed=True).count()


class GoalListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for goal listing"""
    owner = UserSerializer(read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    cards_count = serializers.SerializerMethodField()
    completed_cards_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = [
            'id', 'title', 'description', 'owner', 'target_date', 
            'is_completed', 'completed_at', 'created_at', 'updated_at',
            'progress_percentage', 'is_overdue', 'cards_count', 'completed_cards_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'completed_at']
    
    def get_cards_count(self, obj):
        return obj.cards.count()
    
    def get_completed_cards_count(self, obj):
        return obj.cards.filter(completed=True).count()


class TaskChecklistSerializer(serializers.ModelSerializer):
    """Serializer for TaskChecklist model"""
    class Meta:
        model = TaskChecklist
        fields = [
            'id', 'title', 'is_completed', 'position', 
            'created_at', 'completed_at'
        ]
        read_only_fields = ['created_at', 'completed_at']


class PomodoroSessionSerializer(serializers.ModelSerializer):
    """Serializer for PomodoroSession model"""
    card = CardSerializer(read_only=True)
    
    class Meta:
        model = PomodoroSession
        fields = [
            'id', 'card', 'session_type', 'duration_minutes',
            'started_at', 'completed_at', 'is_completed', 'notes'
        ]
        read_only_fields = ['started_at', 'completed_at']


class TeamMembershipSerializer(serializers.ModelSerializer):
    """Serializer for TeamMembership model"""
    user = UserSerializer(read_only=True)
    invited_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = [
            'id', 'user', 'role', 'joined_at', 'invited_by'
        ]
        read_only_fields = ['joined_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    owner = UserSerializer(read_only=True)
    members = TeamMembershipSerializer(source='teammembership_set', many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'owner', 'members',
            'member_count', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    card = CardSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'title', 'message', 'card', 'goal', 
            'is_read', 'created_at'
        ]
        read_only_fields = ['created_at']


class BoardListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for board listing"""
    owner = UserSerializer(read_only=True)
    lists_count = serializers.SerializerMethodField()
    cards_count = serializers.SerializerMethodField()
    recent_activity = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = [
            'id', 'title', 'description', 'owner', 'created_at', 
            'updated_at', 'is_active', 'lists_count', 'cards_count', 'recent_activity'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_lists_count(self, obj):
        return obj.lists.count()
    
    def get_cards_count(self, obj):
        return Card.objects.filter(list__board=obj).count()
    
    def get_recent_activity(self, obj):
        recent_activities = CardActivity.objects.filter(
            card__list__board=obj
        ).order_by('-created_at')[:3]
        return CardActivitySerializer(recent_activities, many=True).data