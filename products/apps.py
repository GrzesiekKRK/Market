from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def create_defaults_departments(sender, **kwargs):
    from .consts import DEPARTMENTS
    from .models import Department
    departments_to_create = [Department(name=name) for name in DEPARTMENTS]
    Department.objects.bulk_create(departments_to_create)


def create_defaults_category(sender, **kwargs):
    from .consts import CATEGORY_DEPARTMENT_MAP
    from .models import Category
    from .models import Department
    departments = Department.objects.all()
    categories_to_create = []
    for department in departments:
        for name, name_department in CATEGORY_DEPARTMENT_MAP:
            if name_department == department.name:
                categories_to_create.append(Category(name=name, department=department))
    Category.objects.bulk_create(categories_to_create)


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        post_migrate.connect(create_defaults_departments, sender=self)
        post_migrate.connect(create_defaults_category, sender=self)
                
