from decimal import Decimal
from uuid import UUID

from account.account import Account


class TestXMLAccount:
    def test_from_xml(self) -> None:
        account = Account.from_xml(
            """
            <account 
                id="a7cf405f-21ec-41b1-b22e-10298eb42510"
                currency="KZT"
                balance="10"
            />
            """
        )
        assert isinstance(account, Account)
        assert account.id_ == UUID("a7cf405f-21ec-41b1-b22e-10298eb42510")
        assert account.balance == Decimal(10)
        assert account.currency == "KZT"
