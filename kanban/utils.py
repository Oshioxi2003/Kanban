import secrets
import string
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from django.core.cache import cache
from django.db.models import QuerySet
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import re


def generate_unique_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure unique token.
    
    Args:
        length: Length of the token (default: 32)
    
    Returns:
        A unique token string
    """
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Add timestamp hash for extra uniqueness
    timestamp = str(timezone.now().timestamp()).encode()
    hash_suffix = hashlib.sha256(timestamp).hexdigest()[:8]
    
    return f"{token}{hash_suffix}"


def generate_share_token() -> str:
    """Generate a shorter, user-friendly share token"""
    # Use a shorter length for share tokens
    return generate_unique_token(length=16)


def calculate_cache_key(*args) -> str:
    """
    Generate a cache key from multiple arguments.
    
    Args:
        *args: Arguments to include in the cache key
    
    Returns:
        A cache key string
    """
    key_parts = [str(arg) for arg in args]
    return ':'.join(key_parts)


def get_or_set_cache(key: str, func, timeout: int = 300):
    """
    Get value from cache or set it using the provided function.
    
    Args:
        key: Cache key
        func: Function to call if cache miss
        timeout: Cache timeout in seconds (default: 5 minutes)
    
    Returns:
        Cached or computed value
    """
    value = cache.get(key)
    if value is None:
        value = func()
        cache.set(key, value, timeout)
    return value


def invalidate_cache_pattern(pattern: str):
    """
    Invalidate all cache keys matching a pattern.
    
    Args:
        pattern: Cache key pattern to match
    """
    if hasattr(cache, '_cache'):
        # For Redis backend
        cache.delete_pattern(f"*{pattern}*")
    else:
        # For other backends, we need to track keys manually
        # This is a limitation of some cache backends
        pass


def paginate_queryset(queryset: QuerySet, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    Manually paginate a queryset.
    
    Args:
        queryset: Django queryset to paginate
        page: Page number (1-indexed)
        page_size: Number of items per page
    
    Returns:
        Dictionary with pagination data
    """
    total_count = queryset.count()
    total_pages = (total_count + page_size - 1) // page_size
    
    # Ensure page is within valid range
    page = max(1, min(page, total_pages))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    items = list(queryset[start:end])
    
    return {
        'items': items,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_count': total_count,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_previous': page > 1,
            'next_page': page + 1 if page < total_pages else None,
            'previous_page': page - 1 if page > 1 else None
        }
    }


def sanitize_html(html_content: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Args:
        html_content: HTML content to sanitize
    
    Returns:
        Sanitized HTML content
    """
    # Remove script tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove event handlers
    html_content = re.sub(r'\son\w+\s*=\s*["\'].*?["\']', '', html_content, flags=re.IGNORECASE)
    
    # Remove javascript: protocol
    html_content = re.sub(r'javascript:', '', html_content, flags=re.IGNORECASE)
    
    return html_content


def calculate_business_days(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate number of business days between two dates.
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Number of business days
    """
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    days = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            days += 1
        current_date += timedelta(days=1)
    
    return days


def estimate_task_duration(title: str, description: str = '') -> float:
    """
    Estimate task duration based on title and description.
    
    Args:
        title: Task title
        description: Task description
    
    Returns:
        Estimated hours as float
    """
    # Simple heuristic based on keywords
    text = (title + ' ' + description).lower()
    
    # Base estimate
    hours = 2.0
    
    # Adjust based on keywords
    if any(word in text for word in ['simple', 'quick', 'easy', 'minor']):
        hours *= 0.5
    elif any(word in text for word in ['complex', 'difficult', 'major', 'refactor']):
        hours *= 2.0
    
    if any(word in text for word in ['research', 'investigate', 'analyze']):
        hours += 2.0
    
    if any(word in text for word in ['implement', 'develop', 'build']):
        hours += 3.0
    
    if any(word in text for word in ['test', 'qa', 'review']):
        hours += 1.0
    
    if any(word in text for word in ['deploy', 'release', 'migration']):
        hours += 1.5
    
    return min(hours, 8.0)  # Cap at 8 hours


def send_notification_email(user_email: str, subject: str, message: str, html_message: Optional[str] = None):
    """
    Send notification email to user.
    
    Args:
        user_email: Recipient email
        subject: Email subject
        message: Plain text message
        html_message: Optional HTML message
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        # Log error but don't raise to avoid breaking the main flow
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send email to {user_email}: {str(e)}")


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to human-readable string.
    
    Args:
        minutes: Duration in minutes
    
    Returns:
        Formatted string (e.g., "2h 30m")
    """
    if minutes < 60:
        return f"{minutes}m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours}h"
    
    return f"{hours}h {remaining_minutes}m"


def get_week_date_range(date: Optional[datetime] = None) -> tuple[datetime, datetime]:
    """
    Get start and end dates for the week containing the given date.
    
    Args:
        date: Date to get week for (default: today)
    
    Returns:
        Tuple of (week_start, week_end)
    """
    if date is None:
        date = timezone.now()
    
    # Get Monday of the week
    week_start = date - timedelta(days=date.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get Sunday of the week
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    return week_start, week_end


def batch_process(items: List[Any], batch_size: int = 100):
    """
    Process items in batches.
    
    Args:
        items: List of items to process
        batch_size: Size of each batch
    
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def calculate_completion_percentage(completed: int, total: int) -> float:
    """
    Calculate completion percentage safely.
    
    Args:
        completed: Number of completed items
        total: Total number of items
    
    Returns:
        Completion percentage (0-100)
    """
    if total == 0:
        return 0.0 if completed == 0 else 100.0
    
    return round((completed / total) * 100, 1)


def generate_color_from_string(text: str) -> str:
    """
    Generate a consistent color hex code from a string.
    
    Args:
        text: Input string
    
    Returns:
        Hex color code (e.g., "#4A90E2")
    """
    # Create hash from string
    hash_object = hashlib.md5(text.encode())
    hash_hex = hash_object.hexdigest()
    
    # Use first 6 characters for color
    color = f"#{hash_hex[:6]}"
    
    # Ensure the color is not too dark
    r = int(hash_hex[0:2], 16)
    g = int(hash_hex[2:4], 16)
    b = int(hash_hex[4:6], 16)
    
    # If too dark, lighten it
    if (r + g + b) < 200:
        r = min(255, r + 100)
        g = min(255, g + 100)
        b = min(255, b + 100)
        color = f"#{r:02x}{g:02x}{b:02x}"
    
    return color


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def is_valid_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_client_ip(request) -> str:
    """
    Get client IP address from request.
    
    Args:
        request: Django request object
    
    Returns:
        Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calculate_priority_score(priority: str, due_date: Optional[datetime] = None) -> int:
    """
    Calculate priority score for sorting.
    
    Args:
        priority: Priority level (low, medium, high, urgent)
        due_date: Optional due date
    
    Returns:
        Priority score (higher = more important)
    """
    base_scores = {
        'low': 1,
        'medium': 2,
        'high': 3,
        'urgent': 4
    }
    
    score = base_scores.get(priority, 0)
    
    # Add urgency based on due date
    if due_date:
        days_until_due = (due_date - timezone.now()).days
        if days_until_due < 0:  # Overdue
            score += 5
        elif days_until_due <= 1:  # Due today or tomorrow
            score += 3
        elif days_until_due <= 3:  # Due soon
            score += 2
        elif days_until_due <= 7:  # Due this week
            score += 1
    
    return score


def merge_dict_deep(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (overwrites dict1 values)
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dict_deep(result[key], value)
        else:
            result[key] = value
    
    return result


# Export all utility functions
__all__ = [
    'generate_unique_token',
    'generate_share_token',
    'calculate_cache_key',
    'get_or_set_cache',
    'invalidate_cache_pattern',
    'paginate_queryset',
    'sanitize_html',
    'calculate_business_days',
    'estimate_task_duration',
    'send_notification_email',
    'format_duration',
    'get_week_date_range',
    'batch_process',
    'calculate_completion_percentage',
    'generate_color_from_string',
    'truncate_text',
    'is_valid_email',
    'get_client_ip',
    'calculate_priority_score',
    'merge_dict_deep'
]