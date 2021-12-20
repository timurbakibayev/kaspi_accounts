from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from account.account import Account


class ObjectNotFound(ValueError):
    ...


@dataclass
class AccountDatabase(ABC):
    @abstractmethod
    def save(self, account: Account) -> None:
        ...

    @abstractmethod
    def get_objects(self) -> List[Account]:
        ...

    @abstractmethod
    def get_object(self, id_: int) -> Account:
        ...
