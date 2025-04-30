from functools import wraps
from typing import Callable

from django.contrib.auth.models import PermissionDenied


def account_role_required(roles: list[int]) -> Callable:
    def decorator(func: Callable):
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
