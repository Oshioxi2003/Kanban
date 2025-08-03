import openai
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import Card, AIAssistantSuggestion, UserStatistics, Goal
from typing import List, Dict, Any

# AI Assistant for intelligent task management
class KanbanAIAssistant:
    def __init__(self):
        # Use OpenAI API or local LLM
        # For demo purposes, we'll use mock responses
        self.use_mock = not hasattr(settings, 'OPENAI_API_KEY')
        
        if not self.use_mock:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def suggest_task_breakdown(self, card: Card) -> Dict[str, Any]:
        """Suggest how to break down a large task into smaller ones"""
        
        if self.use_mock:
            return self._mock_task_breakdown(card)
        
        prompt = f"""
        Analyze this task and suggest how to break it down into smaller, manageable subtasks:
        
        Task Title: {card.title}
        Description: {card.description or 'No description provided'}
        Priority: {card.priority}
        Due Date: {card.due_date or 'No due date'}
        
        Please provide:
        1. 3-5 specific, actionable subtasks
        2. Estimated time for each subtask
        3. Suggested order of execution
        4. Any dependencies between subtasks
        
        Format as JSON with structure:
        {{
            "subtasks": [
                {{
                    "title": "Subtask title",
                    "description": "Brief description",
                    "estimated_hours": 2,
                    "order": 1,
                    "dependencies": []
                }}
            ],
            "total_estimated_hours": 8,
            "notes": "Additional insights or tips"
        }}
        """
        
        try:
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=800,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].text.strip())
            return result
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._mock_task_breakdown(card)
    
    def _mock_task_breakdown(self, card: Card) -> Dict[str, Any]:
        """Mock task breakdown for development"""
        mock_suggestions = {
            "subtasks": [
                {
                    "title": f"Research and plan for: {card.title}",
                    "description": "Gather requirements and create implementation plan",
                    "estimated_hours": 2,
                    "order": 1,
                    "dependencies": []
                },
                {
                    "title": f"Design solution for: {card.title}",
                    "description": "Create wireframes or technical design",
                    "estimated_hours": 3,
                    "order": 2,
                    "dependencies": [1]
                },
                {
                    "title": f"Implement core functionality: {card.title}",
                    "description": "Build the main features",
                    "estimated_hours": 5,
                    "order": 3,
                    "dependencies": [2]
                },
                {
                    "title": f"Test and refine: {card.title}",
                    "description": "Quality assurance and improvements",
                    "estimated_hours": 2,
                    "order": 4,
                    "dependencies": [3]
                }
            ],
            "total_estimated_hours": 12,
            "notes": "Consider breaking this into smaller milestones. Start with research to better understand scope."
        }
        return mock_suggestions
    
    async def suggest_schedule_optimization(self, user) -> Dict[str, Any]:
        """Suggest optimal schedule based on user's tasks and productivity patterns"""
        
        # Get user's tasks and patterns
        pending_cards = Card.objects.filter(
            list__board__owner=user,
            completed=False
        ).order_by('due_date', 'priority')
        
        # Get user statistics for pattern analysis
        recent_stats = UserStatistics.objects.filter(
            user=user,
            date__gte=timezone.now().date() - timedelta(days=30)
        )
        
        if self.use_mock:
            return self._mock_schedule_optimization(pending_cards)
        
        # Prepare data for AI
        tasks_data = [
            {
                "title": card.title,
                "priority": card.priority,
                "estimated_hours": card.estimated_hours or 2,
                "due_date": card.due_date.isoformat() if card.due_date else None
            }
            for card in pending_cards[:10]  # Limit to top 10 tasks
        ]
        
        prompt = f"""
        Based on these pending tasks and user productivity data, suggest an optimal schedule:
        
        Tasks: {json.dumps(tasks_data, indent=2)}
        
        Provide a weekly schedule suggestion with:
        1. Daily task allocation
        2. Optimal time slots for different types of work
        3. Break recommendations
        4. Buffer time for unexpected tasks
        
        Format as JSON.
        """
        
        try:
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1000,
                temperature=0.6
            )
            
            result = json.loads(response.choices[0].text.strip())
            return result
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._mock_schedule_optimization(pending_cards)
    
    def _mock_schedule_optimization(self, pending_cards) -> Dict[str, Any]:
        """Mock schedule optimization"""
        return {
            "schedule": {
                "Monday": {
                    "morning": "High-priority tasks (9-11 AM)",
                    "afternoon": "Collaborative work (2-4 PM)",
                    "tasks": ["Complete urgent deliverables", "Team meetings"]
                },
                "Tuesday": {
                    "morning": "Deep work sessions (9-12 PM)",
                    "afternoon": "Review and planning (2-3 PM)",
                    "tasks": ["Focus on complex problems", "Weekly planning"]
                },
                "Wednesday": {
                    "morning": "Creative work (9-11 AM)",
                    "afternoon": "Communication and follow-ups (2-5 PM)",
                    "tasks": ["Design and innovation", "Email and calls"]
                }
            },
            "recommendations": [
                "Schedule your most challenging tasks during 9-11 AM (your peak focus time)",
                "Block 2-3 PM for administrative tasks when energy is lower",
                "Reserve Friday afternoons for planning next week",
                "Take 15-minute breaks every 90 minutes for optimal productivity"
            ],
            "productivity_tips": [
                "Use the Pomodoro Technique for focused work sessions",
                "Group similar tasks together to minimize context switching",
                "Set specific time limits for meetings and email checking"
            ]
        }
    
    async def generate_summary(self, user, period: str = 'week') -> Dict[str, Any]:
        """Generate natural language summary of user's work"""
        
        # Calculate date range
        end_date = timezone.now().date()
        if period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=7)
        
        # Get data for the period
        completed_cards = Card.objects.filter(
            list__board__owner=user,
            completed=True,
            completed_at__date__range=[start_date, end_date]
        )
        
        created_cards = Card.objects.filter(
            list__board__owner=user,
            created_at__date__range=[start_date, end_date]
        )
        
        stats = UserStatistics.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        )
        
        if self.use_mock:
            return self._mock_summary(period, completed_cards.count(), created_cards.count())
        
        # Prepare data for AI
        summary_data = {
            "period": period,
            "completed_tasks": completed_cards.count(),
            "created_tasks": created_cards.count(),
            "total_hours": sum(stat.hours_worked for stat in stats),
            "completed_task_titles": [card.title for card in completed_cards[:5]]
        }
        
        prompt = f"""
        Generate a natural language summary of this user's productivity:
        
        {json.dumps(summary_data, indent=2)}
        
        Create an engaging, personalized summary that:
        1. Highlights achievements
        2. Identifies patterns
        3. Provides encouraging feedback
        4. Suggests improvements
        
        Keep it conversational and motivating.
        """
        
        try:
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=400,
                temperature=0.8
            )
            
            return {
                "summary": response.choices[0].text.strip(),
                "stats": summary_data
            }
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._mock_summary(period, completed_cards.count(), created_cards.count())
    
    def _mock_summary(self, period: str, completed: int, created: int) -> Dict[str, Any]:
        """Mock natural language summary"""
        if period == 'week':
            summary = f"""
            Great week! 🎉 You completed {completed} tasks and created {created} new ones. 
            
            Your productivity is on track - you're maintaining a good balance between completing 
            existing work and planning ahead. The fact that you completed {completed} tasks shows 
            you're making steady progress on your goals.
            
            💡 Keep up the momentum! Consider grouping similar tasks together to maximize your focus time.
            """
        else:
            summary = f"""
            Fantastic month! 🚀 You've accomplished {completed} tasks while adding {created} new ones to your pipeline.
            
            This month showed consistent productivity patterns. You're demonstrating excellent task management
            skills by staying on top of your workload while continuously planning ahead.
            
            🎯 Your completion rate suggests you're setting realistic goals and following through effectively.
            Consider celebrating these wins and using this momentum for next month!
            """
        
        return {
            "summary": summary.strip(),
            "stats": {
                "completed_tasks": completed,
                "created_tasks": created,
                "period": period
            }
        }
    
    async def suggest_priorities(self, user) -> List[Dict[str, Any]]:
        """Suggest task priorities using AI analysis"""
        
        # Get user's pending tasks
        pending_cards = Card.objects.filter(
            list__board__owner=user,
            completed=False
        ).order_by('created_at')
        
        if self.use_mock:
            return self._mock_priority_suggestions(pending_cards)
        
        # Analyze tasks for priority suggestions
        suggestions = []
        
        for card in pending_cards[:10]:  # Limit analysis
            suggestion = {
                "card_id": card.id,
                "current_priority": card.priority,
                "suggested_priority": self._calculate_suggested_priority(card),
                "reasoning": self._get_priority_reasoning(card)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _mock_priority_suggestions(self, pending_cards) -> List[Dict[str, Any]]:
        """Mock priority suggestions"""
        suggestions = []
        
        for card in pending_cards[:5]:
            suggestions.append({
                "card_id": card.id,
                "title": card.title,
                "current_priority": card.priority,
                "suggested_priority": "high" if card.due_date and card.due_date < timezone.now() + timedelta(days=3) else "medium",
                "reasoning": "Due date approaching" if card.due_date else "Consider increasing priority based on dependencies"
            })
        
        return suggestions
    
    def _calculate_suggested_priority(self, card: Card) -> str:
        """Calculate suggested priority based on various factors"""
        score = 0
        
        # Due date factor
        if card.due_date:
            days_until_due = (card.due_date.date() - timezone.now().date()).days
            if days_until_due <= 1:
                score += 4
            elif days_until_due <= 3:
                score += 3
            elif days_until_due <= 7:
                score += 2
        
        # Current priority factor
        priority_scores = {'urgent': 4, 'high': 3, 'medium': 2, 'low': 1}
        score += priority_scores.get(card.priority, 2)
        
        # Goal linkage factor
        if card.goal:
            score += 1
        
        # Convert score to priority
        if score >= 6:
            return 'urgent'
        elif score >= 4:
            return 'high'
        elif score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _get_priority_reasoning(self, card: Card) -> str:
        """Get reasoning for priority suggestion"""
        reasons = []
        
        if card.due_date:
            days_until_due = (card.due_date.date() - timezone.now().date()).days
            if days_until_due <= 1:
                reasons.append("Due very soon")
            elif days_until_due <= 3:
                reasons.append("Due within 3 days")
        
        if card.goal:
            reasons.append("Linked to goal")
        
        if not reasons:
            reasons.append("Based on current priority and timeline")
        
        return "; ".join(reasons)


# Utility function to get AI assistant instance
def get_ai_assistant():
    return KanbanAIAssistant()