from dataclasses import dataclass

from ..types import Date


@dataclass
class Bill:
    id: str
    amount: int
    expire: Date
    status: int | str
    shop_id: str
    url: str | None = None
    comment: str | None = None
    fail_url: str | None = None
    success_url: str | None = None
    hook_url: str | None = None
    custom_fields: str | None = None
    merchantName: str | None = None
    exclude_service: list | None = None
    include_service: list | None = None
    error_message: str | None = None
