from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tag, Monster, Mercenary, Contract
from .serializers import (
    TagSerializer,
    MonsterSerializer,
    MercenarySerializer,
    ContractSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MonsterViewSet(viewsets.ModelViewSet):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer


class MercenaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mercenary.objects.select_related("user").all()
    serializer_class = MercenarySerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = (
        Contract.objects.select_related("assigned_to__user")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = ContractSerializer

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        contract = self.get_object()

        if contract.status == Contract.Status.COMPLETED:
            return Response({"error": "Контракт уже завершён"}, status=400)

        if not contract.assigned_to:
            return Response({"error": "У контракта нет назначенного исполнителя."}, status=400)

        mercenary = contract.assinget_to
        mercenary.gold += contract.reward
        mercenary.save(update_fields=["gold"])

        contract.status = Contract.Status.COMPLETED
        contract.save(update_fields=["status"])

        return Response(
            {
                "status": "Контракт успешно выполнен!",
                "mercenary_gold": mercenary.gold,
            }
        )
