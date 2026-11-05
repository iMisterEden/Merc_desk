from rest_framework import permissions


class IsGuildMasterOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj):  # type: ignore[override]
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAssngedMercenary(permissions.BasePermission):

    def has_permission(self, request, view, obj):  # type: ignore[override]
        if request.user.is_staff:
            return True

        if not hasattr(request.user, "mercenary"):
            return False

        return obj.assinget_to == request.user.mercenary
