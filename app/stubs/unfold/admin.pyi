from django.contrib.admin import ModelAdmin as DjangoModelAdmin
from django.db.models import Model

class ModelAdmin(DjangoModelAdmin[Model]): ...
