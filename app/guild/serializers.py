from rest_framework import serializers
from .models import Tag, Monster, Mercenary, Contract


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class MonsterSerializer(serializers.ModelSerializer):
    danger_display = serializers.CharField(source="get_danger_display", read_only=True)

    class Meta:
        model = Monster
        fields = ["id", "name", "description", "experience_gain", "danger", "danger_display"]


class MercenarySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    rank_display = serializers.CharField(source="get_rank_display", read_only=True)

    class Meta:
        model = Mercenary
        fields = [
            "id",
            "username",
            "rank",
            "rank_display",
            "gold",
            "is_injured",
        ]
        read_only_fields = ["gold", "is_injured"]


class ContractSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    assigned_to_detail = MercenarySerializer(source="assigned_to", read_only=True)
    tags_detail = TagSerializer(source="tags", many=True, read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "description",
            "reward",
            "status",
            "status_display",
            "assigned_to",
            "assigned_to_detail",
            "tags",
            "tags_detail",
            "created_at",
        ]

    def validate_reward(self, value):
        if value < 50:
            raise serializers.ValidationError("Награда не может быть меньше 50 золотых монет!")

    def validate(self, attrs):
        assigned_to = attrs.get("assigned_to")
        status = attrs.get("status")

        if assigned_to and assigned_to.is_injured:
            raise serializers.ValidationError(
                {"assigned_to": "Нельзя назначить контракт на раненого наёмника!"}
            )

        if not self.instance and status == Contract.Status.COMPLETED:
            raise serializers.ValidationError(
                {"status": "Новый контракт не может быть сразу завершенным."}
            )

        return attrs
