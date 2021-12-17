import random
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4
import json


class CurrencyMismatchError(ValueError):
    pass


@dataclass
class Account:
    id_: UUID
    currency: str
    balance: Decimal

    def __lt__(self, other: "Account") -> bool:
        assert isinstance(other, Account)
        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.balance < other.balance

    def to_json(self) -> str:
        json_repr = {
            "id": str(self.id_),
            "currency": self.currency,
            "balance": float(self.balance),
        }
        return json.dumps(json_repr)

    @classmethod
    def from_json(cls, json_str: str) -> "Account":  # Factory
        obj = json.loads(json_str)
        assert "id" in obj
        assert "currency" in obj
        assert "balance" in obj
        return Account(
            id_=UUID(obj["id"]),
            currency=obj["currency"],
            balance=Decimal(obj["balance"]),
        )

    @classmethod
    def random(cls) -> "Account":  # Factory
        return Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(random.randint(1, 1000)),
        )
