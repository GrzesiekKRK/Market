from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def has_one_of_roles(context: dict, *roles: tuple) -> bool:
    request = context['request']

    user = request.user
    if not user.is_authenticated:
        return False

    if user.role in roles:
        return True

    return False
