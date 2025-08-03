from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q


class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    # Theme preferences
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    theme_color = models.CharField(max_length=7, default='#3B82F6')  # Primary color
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    due_date_reminders = models.BooleanField(default=True)
    daily_summary = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def name(self):
        """Return display name or username"""
        return self.display_name or self.user.get_full_name() or self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Label(models.Model):
    """Label model for tasks"""
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['name', 'user']
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Goal(models.Model):
    """Goal model for personal objectives"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def progress_percentage(self):
        """Calculate completion percentage based on associated tasks"""
        total_cards = self.cards.count()
        if total_cards == 0:
            return 0
        completed_cards = self.cards.filter(completed=True).count()
        return round((completed_cards / total_cards) * 100, 1)
    
    @property
    def is_overdue(self):
        """Check if goal is overdue"""
        if self.target_date and not self.is_completed:
            return timezone.now().date() > self.target_date
        return False


class Board(models.Model):
    """Model representing a Kanban board"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_template = models.BooleanField(default=False)
    
    # Board customization
    background_color = models.CharField(max_length=7, default='#F3F4F6')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def create_default_lists(self):
        """Create default To-do, Doing, Done lists"""
        default_lists = [
            {'title': 'To-do', 'position': 0},
            {'title': 'Doing', 'position': 1},
            {'title': 'Done', 'position': 2},
        ]
        
        for list_data in default_lists:
            List.objects.create(
                title=list_data['title'],
                board=self,
                position=list_data['position']
            )


class List(models.Model):
    """Model representing a list/column in a Kanban board"""
    title = models.CharField(max_length=200)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position']
        unique_together = ['board', 'position']
    
    def __str__(self):
        return f"{self.board.title} - {self.title}"


class Card(models.Model):
    """Model representing a card in a Kanban list"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='cards')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cards')
    labels = models.ManyToManyField(Label, blank=True, related_name='cards')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    position = models.PositiveIntegerField(default=0)
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.PositiveIntegerField(null=True, blank=True, help_text="Estimated hours to complete")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['position']
        unique_together = ['list', 'position']
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        """Check if card is overdue"""
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False
    
    @property
    def is_due_soon(self):
        """Check if card is due within 24 hours"""
        if self.due_date and not self.completed:
            time_diff = self.due_date - timezone.now()
            return 0 <= time_diff.total_seconds() <= 86400  # 24 hours
        return False
    
    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)
    
    @classmethod
    def search(cls, user, query, filters=None):
        """Advanced search and filter for cards"""
        queryset = cls.objects.filter(list__board__owner=user)
        
        # Text search
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(labels__name__icontains=query)
            ).distinct()
        
        # Apply filters
        if filters:
            # Filter by labels
            if filters.get('labels'):
                queryset = queryset.filter(labels__id__in=filters['labels']).distinct()
            
            # Filter by priority
            if filters.get('priority'):
                queryset = queryset.filter(priority__in=filters['priority'])
            
            # Filter by status
            if filters.get('status'):
                if 'completed' in filters['status']:
                    queryset = queryset.filter(completed=True)
                if 'pending' in filters['status']:
                    queryset = queryset.filter(completed=False)
            
            # Filter by due date
            if filters.get('due_date'):
                if filters['due_date'] == 'overdue':
                    queryset = queryset.filter(
                        due_date__lt=timezone.now(),
                        completed=False
                    )
                elif filters['due_date'] == 'due_soon':
                    due_soon_date = timezone.now() + timezone.timedelta(days=3)
                    queryset = queryset.filter(
                        due_date__lte=due_soon_date,
                        due_date__gte=timezone.now(),
                        completed=False
                    )
                elif filters['due_date'] == 'no_due_date':
                    queryset = queryset.filter(due_date__isnull=True)
            
            # Filter by assignee
            if filters.get('assignee'):
                queryset = queryset.filter(assignee__id__in=filters['assignee'])
            
            # Filter by board
            if filters.get('board'):
                queryset = queryset.filter(list__board__id__in=filters['board'])
            
            # Filter by date range
            if filters.get('created_from'):
                queryset = queryset.filter(created_at__gte=filters['created_from'])
            if filters.get('created_to'):
                queryset = queryset.filter(created_at__lte=filters['created_to'])
        
        return queryset.order_by('-updated_at')


class Comment(models.Model):
    """Model representing comments on cards"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.card.title}"


class CardActivity(models.Model):
    """Model to track card activities for timeline"""
    ACTIVITY_TYPES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('moved', 'Moved'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('commented', 'Commented'),
        ('labeled', 'Labeled'),
        ('goal_linked', 'Goal Linked'),
    ]
    
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} {self.activity_type} {self.card.title}"


class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPES = [
        ('due_soon', 'Due Soon'),
        ('overdue', 'Overdue'),
        ('assigned', 'Assigned'),
        ('mentioned', 'Mentioned'),
        ('goal_progress', 'Goal Progress'),
        ('daily_summary', 'Daily Summary'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class UserStatistics(models.Model):
    """Model to store daily user statistics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statistics')
    date = models.DateField()
    cards_created = models.PositiveIntegerField(default=0)
    cards_completed = models.PositiveIntegerField(default=0)
    cards_moved = models.PositiveIntegerField(default=0)
    hours_worked = models.FloatField(default=0.0)
    pomodoro_sessions = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Team(models.Model):
    """Model for team/workspace management"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField(
        User, 
        through='TeamMembership', 
        through_fields=('team', 'user'),
        related_name='teams'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    """Model for team membership with roles"""
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(default=timezone.now)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_invitations')
    
    class Meta:
        unique_together = ['team', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.team.name} ({self.role})"


class TaskChecklist(models.Model):
    """Model for checklist items within tasks"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='checklist_items')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['position']
        unique_together = ['card', 'position']
    
    def __str__(self):
        return f"{self.card.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)


class PomodoroSession(models.Model):
    """Model for Pomodoro timer sessions"""
    SESSION_TYPES = [
        ('work', 'Work'),
        ('short_break', 'Short Break'),
        ('long_break', 'Long Break'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True, related_name='pomodoro_sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='work')
    duration_minutes = models.PositiveIntegerField(default=25)  # 25 min work, 5 min break, 15 min long break
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.session_type} ({self.duration_minutes}min)"
    
    @property
    def is_break(self):
        return self.session_type in ['short_break', 'long_break']


class AIAssistantSuggestion(models.Model):
    """Model for AI assistant suggestions"""
    SUGGESTION_TYPES = [
        ('task_breakdown', 'Task Breakdown'),
        ('schedule_optimization', 'Schedule Optimization'),
        ('priority_suggestion', 'Priority Suggestion'),
        ('weekly_summary', 'Weekly Summary'),
        ('monthly_summary', 'Monthly Summary'),
        ('productivity_tip', 'Productivity Tip'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_suggestions')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True, related_name='ai_suggestions')
    suggestion_type = models.CharField(max_length=30, choices=SUGGESTION_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    suggested_actions = models.JSONField(default=list, blank=True)  # List of suggested actions
    is_applied = models.BooleanField(default=False)
    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ShareableLink(models.Model):
    """Model for shareable board links"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='shareable_links')
    token = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Share link for {self.board.title}"
    
    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def save(self, *args, **kwargs):
        if not self.token:
            import secrets
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)