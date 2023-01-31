import pytest
import sqlite3
import server.service as service
import time

create_table = '''
            CREATE TABLE IF NOT EXISTS Transactions (
                id uuid not null primary key,
                transaction_id not null,
                group_name text not null,
                purchaser text not null,
                debtor string not null,
                amount real not null,
                is_paid boolean not null,
                memo text not null,
                ip_addr text not null,
                timestamp datetime default current_timestamp
            );
            '''


def setup_db():
    # sqlite here
    # Create a database in RAM
    conn = sqlite3.connect('test.db')
    print("Running setup db")
    # Create a table
    conn.execute(create_table)
    return conn


@pytest.fixture
def Payload():
    payload = {
        "group": "newtest",
        "payer": "cheryl",
        "subtotal": "15.91",
        "tax": "0",
        "tip": "0",
        "memo": "sentra Uber",
        "ip": "0.0.0.0",
        "id": "a47d84fe-612b-45d6-a18e-b45c731d5b22",
        "participants": [
            {
                "name": "cheryl",
                "amount": ""
            },
            {
                "name": "julene",
                "amount": ""
            }
        ]
    }

    return payload


def test_add_transaction_success(Payload, mocker):
    conn = setup_db()

    mocker.patch(
        'sqlite3.connect', return_value=conn
    )
    # mocker.patch(
    #     'sqlite3.connect.close', dumb_func()
    # )
    out = service.add_transaction(Payload)
    time.sleep(1)
    newconn = sqlite3.connect('test.dba')
    output = newconn.execute("select * from Transactions")
    print("This is output" + str(output.fetchone()))
    assert out != None
