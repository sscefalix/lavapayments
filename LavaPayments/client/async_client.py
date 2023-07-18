from hashlib import sha256
from hmac import new
from json import dumps
from uuid import uuid4

from aiohttp import ClientSession, ContentTypeError

from ..exceptions import LavaPaymentsException
from ..types import Service, Bill


class AsyncLavaPayments:
    """
    Асинхронный клиент для работы с Бизнес API Lava.ru

    **Параметры**\n
        • secret_key - ``str`` (required) - Секретный ключ проекта\n
        • project_id - ``str`` (required) - ID проекта
    """

    def __init__(self, secret_key: str, shop_id: str):
        self._secret_key = secret_key
        self._shop_id = shop_id

    @staticmethod
    async def _request(method: str, endpoint: str, *, json: dict | None = None,
                       headers: dict | None = None) -> str | dict:
        if json is None:
            json = {}

        if headers is None:
            headers = {}

        async with ClientSession(headers=headers) as session:
            async with session.request(method, endpoint, json=json) as request:
                try:
                    return await request.json()
                except ContentTypeError:
                    return await request.text()

    def _create_signature(self, data: dict):
        json = dumps(data).encode()
        return new(bytes(self._secret_key, 'UTF-8'), json, sha256).hexdigest()

    def _create_headers(self, data: dict):
        return {
            "Signature": self._create_signature(data),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _create_bill_data(
            self,
            amount: float,
            order_id: str | int | None,
            hook_url: str | None,
            fail_url: str | None,
            success_url: str | None,
            expire: int,
            custom_fields: str | None,
            comment: str | None,
            include_service: list[Service] | None,
            exclude_service: list[Service] | None
    ):
        return {
            "sum": amount,
            "orderId": order_id,
            "shopId": self._shop_id,
            "hookUrl": hook_url,
            "failUrl": fail_url,
            "successUrl": success_url,
            "expire": expire,
            "customFields": custom_fields,
            "comment": comment,
            "includeService": include_service,
            "excludeService": exclude_service
        }

    async def create_bill(
            self,
            amount: float,
            order_id: str | int | None = None,
            hook_url: str | None = None,
            fail_url: str | None = None,
            success_url: str | None = None,
            expire: int = 300,
            custom_fields: str | None = None,
            comment: str | None = None,
            include_service: list[Service] | None = None,
            exclude_service: list[Service] | None = None
    ) -> Bill:
        """
        Выставление счета

        **Параметры**\n
            • amount - ``float`` (required) - Сумма выставленного счета\n
            • order_id - ``str | int`` (optional) - Идентификатор платежа в системе мерчанта\n
            • hook_url - ``str`` (optional) -
            • fail_url - ``str`` (optional) -
            • success_url - ``str`` (optional) -
            • expire - ``int`` (optional) - Время жизни счета в минутах\n
            • custom_fields - ``str`` (optional) -
            • comment - ``str`` (optional) - Комментарий к выставленному счету\n
            • include_service - ``str`` (optional) -
            • exclude_service - ``str`` (optional) -

        :return: ``Bill`` - Объект выставленного счета
        """
        if amount < 1:
            raise LavaPaymentsException("Минимаьная сумма счёта - 1 рубль.")

        if order_id is None:
            order_id = f"LavaPayments_{uuid4()}"

        if expire < 1:
            raise LavaPaymentsException("Минимальное время жизни счёта - 1 минута.")
        elif expire > 43200:
            raise LavaPaymentsException("Максимальное время жизни счёта - 43200 минут.")

        data = self._create_bill_data(
            amount,
            order_id,
            hook_url,
            fail_url,
            success_url,
            expire,
            custom_fields,
            comment,
            include_service,
            exclude_service
        )

        headers = self._create_headers(data)

        request = await self._request("POST", "https://api.lava.ru/business/invoice/create", json=data, headers=headers)

        return Bill(**request.get("data"))

    def _create_get_bill_data(
            self,
            invoice_id: str | None = None,
            order_id: str | int | None = None
    ):
        data = {
            "shopId": self._shop_id
        }

        if invoice_id:
            data.update({"invoiceId": invoice_id})
        elif order_id:
            data.update({"orderId": order_id})
        else:
            raise LavaPaymentsException("Что бы получить счёт нужно передать invoice_id или order_id")

        return data

    async def get_bill(
            self,
            invoice_id: str | None = None,
            order_id: str | int | None = None
    ) -> Bill:
        """
        Получение счёта

        **Параметры**\n
            • invoice_id - ``str`` (required, если не указан ``order_id``) -
            • order_id - ``str | int`` (required, если не указан ``invoice_id``) - Идентификатор платежа в системе мерчанта\n

        :return: ``Bill`` - Объект выставленного счета
        """
        data = self._create_get_bill_data(
            invoice_id,
            order_id
        )

        headers = self._create_headers(data)

        request = await self._request("POST", "https://api.lava.ru/business/invoice/status", json=data, headers=headers)

        return Bill(**request.get("data"))
