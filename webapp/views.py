import json
from uuid import uuid4

from django.http import HttpResponse, HttpRequest
import os

from django.shortcuts import render

from account.account import Account
from database.database import ObjectNotFound
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM

dbname: str = os.environ.get("pg_dbname", "")
if dbname == "":
    database = AccountDatabaseRAM()
    print("Using RAM")
else:
    port:int = 25060
    user:str = os.environ.get("pg_user")
    password:str = os.environ.get("pg_password")
    host:str = "db-postgresql-nyc3-99638-do-user-4060406-0.b.db.ondigitalocean.com"
    connection_str = f"dbname={dbname} port={port} user={user} password={password} host={host}"
    database = AccountDatabasePostgres(connection=connection_str)


def accounts_list(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    return render(request, "index.html", context={"accounts": accounts})


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="""
    <html>
        <body>
           <h1>Hello, World!</h1> 
           <h3>Try to access <a href="/api/accounts/">/api/accounts/</a></h3>
        </body>
    </html>
    """)


def accounts(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()

    if request.method == "GET":
        json_obj = [account.to_json() for account in accounts]
        return HttpResponse(content=json.dumps(json_obj))

    if request.method == "POST":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            account.id_ = uuid4()
            try:
                database.get_object(account.id_)
                return HttpResponse(content=f"Error: object already exists, use PUT to update", status=400)
            except ObjectNotFound:
                database.save(account)
                return HttpResponse(content=account.to_json_str(), status=201)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)

    if request.method == "PUT":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            database.get_object(account.id_)
            database.save(account)
            return HttpResponse(content="OK", status=200)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)
