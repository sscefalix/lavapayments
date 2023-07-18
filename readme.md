# LavaPayments
**Python Библиотека для работы с Бизнес API Lava.ru**

Преимущества
------------
- Асинхронный враппер
- Модели времени и счетов

Установка
---------
**Необходима версия Python 3.8 или выше**

```shell
#Linux
python3 -m pip install -U lavapayments

#Windows
py -3 -m pip install -U lavapayments
```

Пример использования
--------------------

```python
from asyncio import run

from LavaPayments.client import AsyncLavaPayments

client = AsyncLavaPayments("SECRET_KEY", "SHOP_ID")


async def main():
    new_bill = await client.create_bill(100.0)
    print(f"Ссылка на оплату: {new_bill.url}")

    bill = await client.get_bill(new_bill.id)
    print(f"Ваша ссылка истекает в {bill.expire}")


run(main())
```
