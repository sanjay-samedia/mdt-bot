class ActionPermissionMixin:
    """
    Action-permission_classes mapping mixin
    Requires View / ViewSet to have action_permission_classes dictionary defined: Dict[str, List[BasePermission]]
    """
    action_permission_classes = {}

    def get_permissions(self):
        if hasattr(self, 'action_permission_classes'):
            try:
                permission_classes = self.action_permission_classes[self.action]
                return [permission_class() for permission_class in permission_classes]
            except KeyError:
                pass
        return super().get_permissions()


class MethodPermissionMixin:
    """
    Request Method (Uppercase) - Permission mapping mixin
    Requires View / ViewSet to have method_permission_classes dictionary defined: Dict[str, List[BasePermission]]
    """
    method_permission_classes = {}

    def get_permissions(self):
        if hasattr(self, 'method_permission_classes'):
            try:
                permission_classes = self.method_permission_classes[self.request.method]
                return [permission_class() for permission_class in permission_classes]
            except KeyError:
                pass
        return super().get_permissions()


class ActionSerializerMixin:
    """
    Action-serializer mapping mixin
    Requires View / ViewSet to have action_serializers dictionary defined: Dict[str, Serializer]
    """
    action_serializers = {}

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            try:
                return self.action_serializers[self.action]
            except KeyError:
                pass
        return super(ActionSerializerMixin, self).get_serializer_class()
