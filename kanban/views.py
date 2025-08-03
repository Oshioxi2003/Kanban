from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Board, List, Card, Comment, UserProfile, Label, CardActivity, Goal, 
    Notification, UserStatistics, Team, TeamMembership, TaskChecklist, 
    PomodoroSession, AIAssistantSuggestion, ShareableLink
)
from .serializers import (
    BoardSerializer, BoardListSerializer, ListSerializer, 
    CardSerializer, CommentSerializer, UserSerializer, UserProfileSerializer,
    UserRegistrationSerializer, UserLoginSerializer, LabelSerializer, CardActivitySerializer,
    GoalSerializer, GoalListSerializer, NotificationSerializer, TaskChecklistSerializer,
    PomodoroSessionSerializer, TeamSerializer, TeamMembershipSerializer
)
from .ai_assistant import get_ai_assistant


class AuthViewSet(viewsets.ViewSet):
    """Authentication related views"""
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """User registration"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """User login"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh)
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """User logout (blacklist refresh token)"""
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current user profile"""
        user = request.user
        profile_data = {}
        
        # Update user fields
        user_fields = ['first_name', 'last_name', 'email']
        for field in user_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        
        # Update profile fields
        profile_fields = ['display_name', 'bio', 'avatar']
        for field in profile_fields:
            if field in request.data:
                profile_data[field] = request.data[field]
        
        if profile_data:
            profile_serializer = UserProfileSerializer(
                user.profile, data=profile_data, partial=True
            )
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return Response(UserSerializer(user).data)


class LabelViewSet(viewsets.ModelViewSet):
    """ViewSet for Label model"""
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardViewSet(viewsets.ModelViewSet):
    """ViewSet for Board model"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        return BoardSerializer
    
    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        # Create default lists for new board
        board.create_default_lists()
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a board with all its lists and cards"""
        original_board = self.get_object()
        
        with transaction.atomic():
            # Create new board
            new_board = Board.objects.create(
                title=f"{original_board.title} (Copy)",
                description=original_board.description,
                owner=request.user
            )
            
            # Duplicate lists and cards
            for original_list in original_board.lists.all():
                new_list = List.objects.create(
                    title=original_list.title,
                    board=new_board,
                    position=original_list.position
                )
                
                for original_card in original_list.cards.all():
                    new_card = Card.objects.create(
                        title=original_card.title,
                        description=original_card.description,
                        list=new_list,
                        priority=original_card.priority,
                        position=original_card.position,
                        due_date=original_card.due_date,
                        estimated_hours=original_card.estimated_hours
                    )
                    # Copy labels
                    new_card.labels.set(original_card.labels.all())
        
        serializer = self.get_serializer(new_board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get timeline view of board activities"""
        board = self.get_object()
        
        # Get query parameters
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        # Get cards with due dates in the specified period
        cards_with_due_dates = Card.objects.filter(
            list__board=board,
            due_date__gte=start_date,
            due_date__lte=timezone.now() + timedelta(days=days)
        ).order_by('due_date')
        
        # Get recent activities
        activities = CardActivity.objects.filter(
            card__list__board=board,
            created_at__gte=start_date
        ).order_by('-created_at')
        
        return Response({
            'cards_timeline': CardSerializer(cards_with_due_dates, many=True).data,
            'recent_activities': CardActivitySerializer(activities, many=True).data,
            'period': {
                'start': start_date,
                'end': timezone.now() + timedelta(days=days),
                'days': days
            }
        })
    
    @action(detail=True, methods=['get'])
    def due_soon(self, request, pk=None):
        """Get cards that are due soon"""
        board = self.get_object()
        
        # Cards due within next 3 days
        due_soon_date = timezone.now() + timedelta(days=3)
        
        due_soon_cards = Card.objects.filter(
            list__board=board,
            due_date__lte=due_soon_date,
            due_date__gte=timezone.now(),
            completed=False
        ).order_by('due_date')
        
        overdue_cards = Card.objects.filter(
            list__board=board,
            due_date__lt=timezone.now(),
            completed=False
        ).order_by('due_date')
        
        return Response({
            'due_soon': CardSerializer(due_soon_cards, many=True).data,
            'overdue': CardSerializer(overdue_cards, many=True).data
        })


class ListViewSet(viewsets.ModelViewSet):
    """ViewSet for List model"""
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return List.objects.filter(board__owner=self.request.user)
    
    def perform_create(self, serializer):
        board_id = self.request.data.get('board')
        try:
            board = Board.objects.get(id=board_id, owner=self.request.user)
            # Set position to last
            last_position = board.lists.count()
            serializer.save(board=board, position=last_position)
        except Board.DoesNotExist:
            raise ValidationError("Board not found or you don't have permission")
    
    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        """Reorder lists within a board"""
        list_obj = self.get_object()
        new_position = request.data.get('position')
        
        if new_position is not None:
            with transaction.atomic():
                # Get all lists in the same board
                lists = List.objects.filter(board=list_obj.board).order_by('position')
                list_data = list(lists.values_list('id', flat=True))
                
                # Remove current list and insert at new position
                list_data.remove(list_obj.id)
                list_data.insert(new_position, list_obj.id)
                
                # Update positions
                for position, list_id in enumerate(list_data):
                    List.objects.filter(id=list_id).update(position=position)
            
            return Response({'message': 'List reordered successfully'})
        
        return Response({'error': 'Position is required'}, status=status.HTTP_400_BAD_REQUEST)


class CardViewSet(viewsets.ModelViewSet):
    """ViewSet for Card model"""
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Card.objects.filter(list__board__owner=self.request.user)
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(labels__name__icontains=search)
            ).distinct()
        
        # Filter by list
        list_id = self.request.query_params.get('list')
        if list_id:
            queryset = queryset.filter(list_id=list_id)
        
        # Filter by labels
        labels = self.request.query_params.getlist('labels')
        if labels:
            queryset = queryset.filter(labels__id__in=labels).distinct()
        
        # Filter by priority
        priorities = self.request.query_params.getlist('priority')
        if priorities:
            queryset = queryset.filter(priority__in=priorities)
        
        # Filter by assignee
        assignee = self.request.query_params.get('assignee')
        if assignee:
            queryset = queryset.filter(assignee_id=assignee)
        
        # Filter by status
        statuses = self.request.query_params.getlist('status')
        if statuses:
            if 'completed' in statuses and 'pending' not in statuses:
                queryset = queryset.filter(completed=True)
            elif 'pending' in statuses and 'completed' not in statuses:
                queryset = queryset.filter(completed=False)
        
        # Filter by due date
        due_filter = self.request.query_params.get('due_date')
        if due_filter == 'overdue':
            queryset = queryset.filter(due_date__lt=timezone.now(), completed=False)
        elif due_filter == 'due_soon':
            due_soon_date = timezone.now() + timedelta(days=3)
            queryset = queryset.filter(
                due_date__lte=due_soon_date,
                due_date__gte=timezone.now(),
                completed=False
            )
        elif due_filter == 'no_due_date':
            queryset = queryset.filter(due_date__isnull=True)
        
        # Filter by board
        boards = self.request.query_params.getlist('board')
        if boards:
            queryset = queryset.filter(list__board__id__in=boards)
        
        # Filter by date range
        created_from = self.request.query_params.get('created_from')
        if created_from:
            queryset = queryset.filter(created_at__gte=created_from)
        
        created_to = self.request.query_params.get('created_to')
        if created_to:
            queryset = queryset.filter(created_at__lte=created_to)
        
        return queryset.order_by('list__position', 'position')
    
    def perform_create(self, serializer):
        list_id = self.request.data.get('list')
        try:
            list_obj = List.objects.get(id=list_id, board__owner=self.request.user)
            # Set position to last
            last_position = list_obj.cards.count()
            serializer.save(list=list_obj, position=last_position)
        except List.DoesNotExist:
            raise ValidationError("List not found or you don't have permission")
    
    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """Move card to different list and/or position"""
        card = self.get_object()
        new_list_id = request.data.get('list_id')
        new_position = request.data.get('position', 0)
        
        try:
            new_list = List.objects.get(id=new_list_id, board__owner=request.user)
            
            with transaction.atomic():
                old_list = card.list
                old_position = card.position
                
                card.list = new_list
                card.position = new_position
                card.save()
                
                # Create activity
                CardActivity.objects.create(
                    card=card,
                    user=request.user,
                    activity_type='moved',
                    description=f"Moved card from '{old_list.title}' to '{new_list.title}'"
                )
                
                # Reorder cards in both lists
                self._reorder_cards(old_list)
                if old_list != new_list:
                    self._reorder_cards(new_list)
            
            serializer = self.get_serializer(card)
            return Response(serializer.data)
            
        except List.DoesNotExist:
            return Response({'error': 'List not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def _reorder_cards(self, list_obj):
        """Helper method to reorder cards in a list"""
        cards = list_obj.cards.order_by('position')
        for index, card in enumerate(cards):
            if card.position != index:
                card.position = index
                card.save(update_fields=['position'])


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(card__list__board__owner=self.request.user)
    
    def perform_create(self, serializer):
        card_id = self.request.data.get('card')
        try:
            card = Card.objects.get(id=card_id, list__board__owner=self.request.user)
            comment = serializer.save(author=self.request.user, card=card)
            
            # Create activity
            CardActivity.objects.create(
                card=card,
                user=self.request.user,
                activity_type='commented',
                description=f"Added a comment"
            )
        except Card.DoesNotExist:
            raise ValidationError("Card not found or you don't have permission")


class GoalViewSet(viewsets.ModelViewSet):
    """ViewSet for Goal model"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GoalListSerializer
        return GoalSerializer
    
    def get_queryset(self):
        return Goal.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark goal as completed"""
        goal = self.get_object()
        goal.is_completed = True
        goal.completed_at = timezone.now()
        goal.save()
        
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Reopen completed goal"""
        goal = self.get_object()
        goal.is_completed = False
        goal.completed_at = None
        goal.save()
        
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def link_card(self, request, pk=None):
        """Link a card to this goal"""
        goal = self.get_object()
        card_id = request.data.get('card_id')
        
        try:
            card = Card.objects.get(
                id=card_id, 
                list__board__owner=request.user
            )
            card.goal = goal
            card.save()
            
            # Create activity
            CardActivity.objects.create(
                card=card,
                user=request.user,
                activity_type='goal_linked',
                description=f"Linked to goal '{goal.title}'"
            )
            
            return Response({'message': 'Card linked to goal successfully'})
        except Card.DoesNotExist:
            return Response(
                {'error': 'Card not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def unlink_card(self, request, pk=None):
        """Unlink a card from this goal"""
        goal = self.get_object()
        card_id = request.data.get('card_id')
        
        try:
            card = Card.objects.get(
                id=card_id, 
                goal=goal,
                list__board__owner=request.user
            )
            card.goal = None
            card.save()
            
            return Response({'message': 'Card unlinked from goal successfully'})
        except Card.DoesNotExist:
            return Response(
                {'error': 'Card not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification model"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().update(is_read=True)
        return Response({'message': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count        })


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team management"""
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Team.objects.filter(
            Q(owner=self.request.user) | 
            Q(members=self.request.user)
        ).distinct()
    
    def perform_create(self, serializer):
        team = serializer.save(owner=self.request.user)
        # Add owner as admin member
        TeamMembership.objects.create(
            team=team,
            user=self.request.user,
            role='owner'
        )
    
    @action(detail=True, methods=['post'])
    def invite_member(self, request, pk=None):
        """Invite a user to join the team"""
        team = self.get_object()
        email = request.data.get('email')
        role = request.data.get('role', 'member')
        
        try:
            user_to_invite = User.objects.get(email=email)
            
            # Check if user is already a member
            if TeamMembership.objects.filter(team=team, user=user_to_invite).exists():
                return Response(
                    {'error': 'User is already a team member'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create membership
            membership = TeamMembership.objects.create(
                team=team,
                user=user_to_invite,
                role=role,
                invited_by=request.user
            )
            
            return Response(TeamMembershipSerializer(membership).data)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User with this email does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class ImportExportViewSet(viewsets.ViewSet):
    """Import/Export functionality"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def create_share_link(self, request):
        """Create a shareable read-only link for a board"""
        board_id = request.data.get('board_id')
        expires_days = request.data.get('expires_days', 30)
        
        try:
            board = Board.objects.get(id=board_id, owner=request.user)
            
            # Create shareable link
            expires_at = timezone.now() + timedelta(days=expires_days)
            
            share_link = ShareableLink.objects.create(
                board=board,
                created_by=request.user,
                expires_at=expires_at
            )
            
            return Response({
                'share_url': f"/shared/{share_link.token}",
                'token': share_link.token,
                'expires_at': share_link.expires_at
            })
            
        except Board.DoesNotExist:
            return Response(
                {'error': 'Board not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model (read-only)"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class AIAssistantViewSet(viewsets.ViewSet):
    """AI Assistant endpoints"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    async def suggest_task_breakdown(self, request):
        """Get AI suggestions for breaking down a task"""
        card_id = request.data.get('card_id')
        
        try:
            card = Card.objects.get(id=card_id, list__board__owner=request.user)
            ai_assistant = get_ai_assistant()
            
            suggestions = await ai_assistant.suggest_task_breakdown(card)
            
            # Save suggestion to database
            ai_suggestion = AIAssistantSuggestion.objects.create(
                user=request.user,
                card=card,
                suggestion_type='task_breakdown',
                title=f"Task breakdown for: {card.title}",
                content=json.dumps(suggestions),
                suggested_actions=suggestions.get('subtasks', [])
            )
            
            return Response({
                'suggestion_id': ai_suggestion.id,
                'suggestions': suggestions
            })
            
        except Card.DoesNotExist:
            return Response({'error': 'Card not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['post'])
    async def suggest_schedule(self, request):
        """Get AI schedule optimization suggestions"""
        try:
            ai_assistant = get_ai_assistant()
            suggestions = await ai_assistant.suggest_schedule_optimization(request.user)
            
            # Save suggestion
            ai_suggestion = AIAssistantSuggestion.objects.create(
                user=request.user,
                suggestion_type='schedule_optimization',
                title="Weekly schedule optimization",
                content=json.dumps(suggestions)
            )
            
            return Response({
                'suggestion_id': ai_suggestion.id,
                'suggestions': suggestions
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['post'])
    async def generate_summary(self, request):
        """Generate natural language summary"""
        period = request.data.get('period', 'week')  # week or month
        
        try:
            ai_assistant = get_ai_assistant()
            summary = await ai_assistant.generate_summary(request.user, period)
            
            # Save suggestion
            ai_suggestion = AIAssistantSuggestion.objects.create(
                user=request.user,
                suggestion_type=f'{period}ly_summary',
                title=f"{period.capitalize()} Summary",
                content=json.dumps(summary)
            )
            
            return Response({
                'suggestion_id': ai_suggestion.id,
                'summary': summary
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['post'])
    async def suggest_priorities(self, request):
        """Get AI priority suggestions"""
        try:
            ai_assistant = get_ai_assistant()
            suggestions = await ai_assistant.suggest_priorities(request.user)
            
            return Response({'suggestions': suggestions})
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['get'])
    def get_suggestions(self, request):
        """Get user's AI suggestions history"""
        suggestions = AIAssistantSuggestion.objects.filter(
            user=request.user
        ).order_by('-created_at')[:20]
        
        return Response({
            'suggestions': [
                {
                    'id': s.id,
                    'type': s.suggestion_type,
                    'title': s.title,
                    'content': s.content,
                    'is_applied': s.is_applied,
                    'created_at': s.created_at
                }
                for s in suggestions
            ]
        })


class TaskChecklistViewSet(viewsets.ModelViewSet):
    """ViewSet for managing task checklist items"""
    serializer_class = TaskChecklistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        card_id = self.request.query_params.get('card')
        if card_id:
            return TaskChecklist.objects.filter(
                card_id=card_id,
                card__list__board__owner=self.request.user
            )
        return TaskChecklist.objects.none()
    
    def perform_create(self, serializer):
        card_id = self.request.data.get('card')
        try:
            card = Card.objects.get(id=card_id, list__board__owner=self.request.user)
            
            # Auto-assign position
            max_position = TaskChecklist.objects.filter(card=card).aggregate(
                models.Max('position')
            )['position__max'] or 0
            
            serializer.save(card=card, position=max_position + 1)
        except Card.DoesNotExist:
            raise ValidationError("Card not found")
    
    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        """Toggle checklist item completion"""
        item = self.get_object()
        item.is_completed = not item.is_completed
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Reorder checklist items"""
        items_data = request.data.get('items', [])
        
        for item_data in items_data:
            try:
                item = TaskChecklist.objects.get(
                    id=item_data['id'],
                    card__list__board__owner=request.user
                )
                item.position = item_data['position']
                item.save()
            except TaskChecklist.DoesNotExist:
                continue
        
        return Response({'message': 'Items reordered successfully'})


class EisenhowerMatrixView(viewsets.ViewSet):
    """Eisenhower Matrix for task prioritization"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def matrix(self, request):
        """Get tasks organized in Eisenhower Matrix"""
        cards = Card.objects.filter(
            list__board__owner=request.user,
            completed=False
        )
        
        # Categorize tasks based on urgency and importance
        matrix = {
            'urgent_important': [],     # Do First (Quadrant 1)
            'not_urgent_important': [], # Schedule (Quadrant 2)
            'urgent_not_important': [], # Delegate (Quadrant 3)
            'not_urgent_not_important': [] # Eliminate (Quadrant 4)
        }
        
        for card in cards:
            # Determine urgency (based on due date)
            is_urgent = False
            if card.due_date:
                days_until_due = (card.due_date.date() - timezone.now().date()).days
                is_urgent = days_until_due <= 2  # Due within 2 days
            
            # Determine importance (based on priority and goal linkage)
            is_important = card.priority in ['high', 'urgent'] or card.goal is not None
            
            # Categorize
            if is_urgent and is_important:
                quadrant = 'urgent_important'
            elif not is_urgent and is_important:
                quadrant = 'not_urgent_important'
            elif is_urgent and not is_important:
                quadrant = 'urgent_not_important'
            else:
                quadrant = 'not_urgent_not_important'
            
            matrix[quadrant].append(CardSerializer(card).data)
        
        return Response({
            'matrix': matrix,
            'quadrant_info': {
                'urgent_important': {
                    'title': 'Do First',
                    'description': 'Urgent and important tasks that need immediate attention',
                    'color': 'red',
                    'action': 'Do immediately'
                },
                'not_urgent_important': {
                    'title': 'Schedule',
                    'description': 'Important but not urgent - plan and schedule these',
                    'color': 'blue',
                    'action': 'Schedule for later'
                },
                'urgent_not_important': {
                    'title': 'Delegate',
                    'description': 'Urgent but not important - consider delegating',
                    'color': 'yellow',
                    'action': 'Delegate if possible'
                },
                'not_urgent_not_important': {
                    'title': 'Eliminate',
                    'description': 'Neither urgent nor important - eliminate or minimize',
                    'color': 'gray',
                    'action': 'Eliminate or do last'
                }
            }
        })
    
    @action(detail=False, methods=['post'])
    def move_card(self, request):
        """Move card to different quadrant by updating priority/due date"""
        card_id = request.data.get('card_id')
        quadrant = request.data.get('quadrant')
        
        try:
            card = Card.objects.get(id=card_id, list__board__owner=request.user)
            
            # Update card based on target quadrant
            if quadrant == 'urgent_important':
                card.priority = 'urgent'
                if not card.due_date:
                    card.due_date = timezone.now() + timedelta(days=1)
            elif quadrant == 'not_urgent_important':
                card.priority = 'high'
                if card.due_date and card.due_date <= timezone.now() + timedelta(days=2):
                    card.due_date = timezone.now() + timedelta(days=7)
            elif quadrant == 'urgent_not_important':
                card.priority = 'medium'
                if not card.due_date:
                    card.due_date = timezone.now() + timedelta(days=1)
            else:  # not_urgent_not_important
                card.priority = 'low'
                card.due_date = None
            
            card.save()
            
            return Response({'message': 'Card moved successfully'})
            
        except Card.DoesNotExist:
            return Response({'error': 'Card not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def apply_suggestion(self, request, pk=None):
        """Mark suggestion as applied"""
        try:
            suggestion = AIAssistantSuggestion.objects.get(
                id=pk, 
                user=request.user
            )
            suggestion.is_applied = True
            suggestion.applied_at = timezone.now()
            suggestion.save()
            
            return Response({'message': 'Suggestion applied successfully'})
            
        except AIAssistantSuggestion.DoesNotExist:
            return Response({'error': 'Suggestion not found'}, status=404)


class PomodoroViewSet(viewsets.ModelViewSet):
    """Pomodoro timer sessions management"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PomodoroSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete_session(self, request, pk=None):
        """Mark Pomodoro session as completed"""
        session = self.get_object()
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()
        
        # Update user statistics
        today = timezone.now().date()
        stats, created = UserStatistics.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={'pomodoro_sessions': 0}
        )
        stats.pomodoro_sessions += 1
        if session.session_type == 'work':
            stats.hours_worked += session.duration_minutes / 60
        stats.save()
        
        return Response({'message': 'Session completed'})
    
    @action(detail=False, methods=['get'])
    def get_stats(self, request):
        """Get Pomodoro statistics"""
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        # Today's sessions
        today_sessions = self.get_queryset().filter(
            started_at__date=today,
            is_completed=True
        )
        
        # This week's sessions
        week_sessions = self.get_queryset().filter(
            started_at__date__gte=week_ago,
            is_completed=True
        )
        
        return Response({
            'today': {
                'total_sessions': today_sessions.count(),
                'work_sessions': today_sessions.filter(session_type='work').count(),
                'total_minutes': sum(s.duration_minutes for s in today_sessions)
            },
            'this_week': {
                'total_sessions': week_sessions.count(),
                'work_sessions': week_sessions.filter(session_type='work').count(),
                'total_minutes': sum(s.duration_minutes for s in week_sessions)
            }
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for the user"""
    user = request.user
    
    # Basic stats
    total_boards = Board.objects.filter(owner=user, is_active=True).count()
    total_cards = Card.objects.filter(list__board__owner=user).count()
    completed_cards = Card.objects.filter(list__board__owner=user, completed=True).count()
    
    # Due soon cards
    due_soon_cards = Card.objects.filter(
        list__board__owner=user,
        due_date__lte=timezone.now() + timedelta(days=3),
        due_date__gte=timezone.now(),
        completed=False
    ).count()
    
    # Overdue cards
    overdue_cards = Card.objects.filter(
        list__board__owner=user,
        due_date__lt=timezone.now(),
        completed=False
    ).count()
    
    # Pomodoro stats
    today = timezone.now().date()
    today_pomodoros = PomodoroSession.objects.filter(
        user=user,
        started_at__date=today,
        is_completed=True,
        session_type='work'
    ).count()
    
    # Recent activity
    recent_activities = CardActivity.objects.filter(
        card__list__board__owner=user
    ).order_by('-created_at')[:10]
    
    return Response({
        'stats': {
            'total_boards': total_boards,
            'total_cards': total_cards,
            'completed_cards': completed_cards,
            'completion_rate': round((completed_cards / total_cards * 100) if total_cards > 0 else 0, 1),
            'due_soon_cards': due_soon_cards,
            'overdue_cards': overdue_cards,
            'today_pomodoros': today_pomodoros
        },
        'recent_activities': CardActivitySerializer(recent_activities, many=True).data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def shared_board_view(request, token):
    """View shared board by token"""
    try:
        # Find board by token (assuming you have a token field in Board model)
        board = Board.objects.get(share_token=token, is_shared=True)
        
        # Get board data with lists and cards
        lists = List.objects.filter(board=board).order_by('position')
        lists_data = []
        
        for list_obj in lists:
            cards = Card.objects.filter(list=list_obj).order_by('position')
            cards_data = CardSerializer(cards, many=True).data
            
            lists_data.append({
                'id': list_obj.id,
                'title': list_obj.title,
                'position': list_obj.position,
                'cards': cards_data
            })
        
        return Response({
            'board': {
                'id': board.id,
                'title': board.title,
                'description': board.description,
                'lists': lists_data
            }
        })
        
    except Board.DoesNotExist:
        return Response({'error': 'Board not found or not shared'}, status=404)