from django.contrib import admin
from .models import Tag, Mercenary, Contract, Monster


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("name",)


@admin.register(Mercenary)
class MercenaryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rank", "gold", "is_injured",)
    list_filter = ("id", "user",)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "reward", "status", "assigned_to", "created_at")
    list_filter = ("status", "tags")
    search_fields = ("title", "description")
    filter_horizontal = ("tags",)


@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "danger", "experience_gain")
    list_filter = ("danger",)
    search_fields = ("name",)
