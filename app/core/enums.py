import enum

class TodoStatus(enum.Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    
    
class TodoPriority(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    

class UserRole(enum.Enum):
    user = 'user'
    admin = 'admin'