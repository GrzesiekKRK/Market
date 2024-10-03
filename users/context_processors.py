from . import consts as users_role


def roles(request) -> dict[str, int]:
    return {
        'CUSTOMER_USER_ROLE': users_role.CUSTOMER_USER_ROLE,
        'CUSTOMER_USER_ROLE_VENDOR': users_role.CUSTOMER_USER_ROLE_VENDOR,
        'CUSTOMER_USER_ROLE_MODERATOR': users_role.CUSTOMER_USER_ROLE_MODERATOR,
    }
