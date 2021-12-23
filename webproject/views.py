from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from account.account import Account
from database.database import AccountDatabase
from database.implementations.ram import AccountDatabaseRAM
import json

database = AccountDatabaseRAM()
for i in range(3):
    database.save(Account.random())


# Create your views here.
def accounts(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        all_accounts = database.get_objects()
        json_view = json.dumps([account.to_json() for account in all_accounts])
        return HttpResponse(content=json_view)
