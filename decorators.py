from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    """
    Decorator to restrict route access to specific roles.
    Usage: @role_required('Super Admin', 'Medical Expert')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.role.name not in roles:
                return abort(403) # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
