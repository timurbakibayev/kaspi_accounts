from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


class CurrencyMismatchError(ValueError):
    pass


@dataclass
class Account:
    id_: UUID
    currency: str
    balance: Decimal

    def __lt__(self, other):
        assert isinstance(other, Account)
        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.balance < other.balance
