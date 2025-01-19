from functools import wraps

from django.contrib.auth.models import PermissionDenied


def account_role_required(roles):  # missed type_hints Callable etc.
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            customer_user = request.user

            if not request.user:
                raise PermissionDenied

            elif customer_user.role not in roles:
                raise PermissionDenied

            return func(request, *args, **kwargs)

        return inner

    return decorator
