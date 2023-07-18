from datetime import datetime

from ..exceptions import LavaPaymentsException


class Date:
    def __init__(self, _date: str) -> None:
        try:
            self._date = datetime.fromisoformat(_date)
        except ValueError:
            raise LavaPaymentsException(f"Не удалось конвертировать дату '{_date}'")

    @property
    def is_expired(self) -> bool:
        return self._date.timestamp() < datetime.now().timestamp()

    def __repr__(self):
        return f'Date(_date={self._date})'

    def __str__(self):
        return self._date
