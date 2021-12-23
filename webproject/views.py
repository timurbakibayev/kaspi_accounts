from django.http import HttpRequest, HttpResponse
from account.account import Account
from database.implementations.ram import AccountDatabaseRAM
import json

database = AccountDatabaseRAM()
if len(database.get_objects()) == 0:
    for i in range(3):
        database.save(Account.random())


# Create your views here.
def accounts(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        all_accounts = database.get_objects()
        json_view = json.dumps([account.to_json() for account in all_accounts])
        return HttpResponse(content=json_view)

    if request.method == "POST":
        try:
            account = Account.from_json_str(request.body.decode("UTF-8"))
            database.save(account)
            return HttpResponse(content=account.to_json_str())
        except Exception as e:
            return HttpResponse(content=str(e), status=400)
