from typing import Any

class DjangoObjectActions:
    change_actions: list[str]
    changelist_actions: list[str]
    def get_change_actions(self, request: Any, object_id: Any, form_url: Any) -> list[str]: ...
    def get_changelist_actions(self, request: Any) -> list[str]: ...
