from dataclasses import dataclass
from typing import List
from uuid import UUID

from account.account import Account


@dataclass
class Customer:
    id_: UUID
    age: int
    first_name: str
    last_name: str
    accounts: List[Account]

    def __lt__(self, other) -> bool:
        return self.age < other.age or self.last_name < other.last_name or self.first_name <= other.first_name
