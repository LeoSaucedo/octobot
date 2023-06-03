import sqlite3
import uuid
import json
import operator

import functools

print = functools.partial(print, flush=True)


def add_transaction(payload):
    '''
    Insert payload values into the database
    Calculate the amount by adding tax and tip to the subtotal

    Payload example:
    {
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

    :return: transaction_id of the transaction that was added
    '''

    print("Inside add transaction function with payload: " + str(payload))

    audit_id = audit_request(payload=payload, audit_id=str(
        uuid.uuid4()), status="IN_PROGRESS")

    try:
        print("Validating payload")
        validate_payload(payload)
        # Fill any missing values with default values
        if payload["tax"] is None:
            payload["tax"] = 0
        if payload["tip"] is None:
            payload["tip"] = 0
        if "ip" not in payload or payload["ip"] is None:
            payload["ip"] = ""
        if "id" not in payload:
            # If id is not present in the payload, generate one.
            payload["id"] = str(uuid.uuid4())

        # Check if participants contains the payer name.
        # Set default values for blank participant amounts.
        payer_in_participants = False
        for participant in payload["participants"]:
            if participant["amount"] is None:
                participant["amount"] = ""
            if (participant["name"] == payload["payer"]):
                payer_in_participants = True

        # If the payer is not in the participants list, add them.
        if (payer_in_participants == False):
            participant = {
                "name": payload["payer"],
                "amount": ""
            }
            payload["participants"].append(participant)

        # Initialize variables for each participant type
        # amount = None
        even_split_participants = []
        uneven_split_participants = []

        # Sort each participant into their respective type
        for participant in payload["participants"]:
            if participant['amount'] == "" or participant['amount'] is None:
                even_split_participants.append(participant)
            else:
                uneven_split_participants.append(participant)

        tax_percent = float(payload["tax"]) / float(payload["subtotal"])
        tip_percent = float(payload["tip"]) / float(payload["subtotal"])

        # Total amount owed by uneven splitters
        total_uneven_split_amount = 0

        # Iterate through the uneven splitters.
        # Calculate the amount each participant owes, and adding their tax and tip.
        # Add the transaction to the database.
        for uneven_split_participant in uneven_split_participants:
            amount = float(uneven_split_participant["amount"])+(float(uneven_split_participant["amount"])
                                                                * tax_percent)+(float(uneven_split_participant["amount"])*tip_percent)
            total_uneven_split_amount += amount

            # Don't add the participant to the database if they are the payer.
            # E.g. Cheryl owes Cheryl $10.00
            if uneven_split_participant["name"] == payload["payer"]:
                continue
            insert_transaction(payload["id"], payload["group"], payload["payer"],
                               uneven_split_participant["name"], amount, payload["memo"], payload["ip"])

        # Calculate the amount each even splitter owes.
        # First, we calculate the total even split amount.
        # even_split_amount = (total amount - total uneven split amount) / number of even splitters
        # Set the amount of each even splitter to even_split_amount.
        # And add the transaction to the database.
        if len(even_split_participants) > 0:
            even_split_amount = ((float(payload["subtotal"]) + float(payload["tax"]) + float(
                payload["tip"])) - total_uneven_split_amount) / len(even_split_participants)

        for even_split_participant in even_split_participants:
            # Don't add the participant to the database if they are the payer.
            if even_split_participant["name"] == payload["payer"]:
                continue
            insert_transaction(payload["id"], payload["group"], payload["payer"],
                               even_split_participant["name"], even_split_amount, payload["memo"], payload["ip"])
    except Exception as e:
        print("Exception occurred while processing transaction: " + str(e))
        audit_request(payload=payload, status="FAILED",
                      audit_id=audit_id, error_msg=str(e))
        raise e
    audit_request(payload=payload, status="SUCCESS", audit_id=audit_id)
    return payload["id"]


def delete_transaction(transaction_id):
    '''
    Delete a transaction from the database.
    This is achieved by setting is_deleted=1 in the DB.
    :return: None
    '''
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("update Transactions set is_deleted=1 where transaction_id=?",
                   (transaction_id,))
    conn.commit()
    conn.close()


def get_transactions(group_name):
    '''
    Get all transactions for a given group.
    :return: List of transactions for the given group.
    '''
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("select transaction_id, purchaser, debtor, amount, memo, timestamp from Transactions where group_name=? and is_paid=0 and is_deleted=0 order by timestamp desc",
                   (group_name,))
    raw_transactions = cursor.fetchall()
    conn.close()
    '''
    transaction object.
    "transactions": [
        {
            "id": "abc",
            "purchaser": "cheryl",
            "memo": "sentra Uber",
            "timestamp": "2019-01-01 12:00:00",
            "participants": [
                {
                    "name": "julene",
                    "amount": 25
                }
            ]
        }
    ]
    '''
    transactions = []
    for raw_transaction in raw_transactions:
        transaction_id = raw_transaction['transaction_id']
        # Check to see if the transaction has already been added to the list.
        # If it has, add the debtor to the list of participants.
        # If it hasn't, create a new transaction object and add it to the list.
        transaction_exists = False
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction_exists = True
                transaction["participants"].append(
                    {"name": raw_transaction["debtor"], "amount": raw_transaction["amount"]})
        if transaction_exists == False:
            transactions.append(
                {"id": transaction_id, "purchaser": raw_transaction["purchaser"], "memo": raw_transaction["memo"], "timestamp": raw_transaction["timestamp"], "participants": [{"name": raw_transaction["debtor"], "amount": raw_transaction["amount"]}]})
    return transactions


def insert_transaction(transaction_id, group_name, purchaser, debtor, amount, memo, ip):
    '''
    Insert transaction into the database
    '''
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO Transactions(id,transaction_id,group_name,purchaser,debtor,amount,is_paid,memo,ip_addr) VALUES (?,?,?,?,?,?,?,?,?)",
                 (str(uuid.uuid4()), transaction_id, group_name, purchaser, debtor, amount, 0, memo, ip))
    conn.commit()
    conn.close()


def dict_factory(cursor, row):
    '''
    Convert database rows into dictionaries
    :return: Dictionary containing the database row
    :disclaimer: grabbed this from the internet
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_rows(transaction_id):
    '''
    Get all rows from the database for a given transaction_id.
    :return: List of dictionaries containing the database rows.
    '''
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cursor = conn.execute(
        "SELECT * FROM Transactions WHERE transaction_id = ?", (transaction_id,))
    rows = cursor.fetchall()
    return rows


def generate_report(group_name, reset_tab, simplify=False):
    '''
    Generates a report for the given group name.


    :param group_name: Name of the group to generate a report for
    :param reset_tab: Boolean indicating whether or not to reset the tab
    :param simplify: Boolean indicating whether or not to simplify the debts
    :return: List of strings in the format of "x owes y $amount"
    '''

    '''
    debtor_dict:
    A 2-D Dictionary containing the debtor and the amount they owe each recipient.
    Example:
    {
        "julene":
            {
                "cheryl": 7.955,
                "david": 56.75
            },
        "cheryl":
            {
                "david": 56.75
            }
    }

    This represents the following:
    - Julene owes Cheryl $7.955
    - Julene owes David $56.75
    - Cheryl owes David $56.75
    '''
    debtor_dict = {}

    '''
    Get all transactions from the group that haven't been paid

    Transaction format:
    id uuid not null primary key,
    transaction_id not null,
    group_name text not null,
    purchaser text not null,
    debtor string not null,
    amount real not null,
    is_paid boolean not null,
    is_deleted boolean not null,
    ip_addr text not null,
    memo text not null
    '''
    conn = sqlite3.connect('database.db')
    cursor = conn.execute(
        "SELECT * FROM Transactions WHERE group_name = ? and is_paid = ? and is_deleted = ?", (group_name, 0, 0))

    # Array of unpaid transactions for the given group
    transactions = cursor.fetchall()

    for transaction in transactions:
        # Grab debtor, recipient, and amount from the transaction.
        debtor = transaction[4]
        recipient = transaction[3]
        amount = transaction[5]

        # If the recipient owes any money to anyone
        if recipient in debtor_dict:
            # If the recipient owes the debtor any money
            if debtor in debtor_dict[recipient]:
                # Get the amount the recipient currently owes the debtor
                recipient_debt = debtor_dict[recipient][debtor]

                # Calculate the amount the debtor owes after this transaction
                debtor_debt_after_transaction = amount - recipient_debt

                # If after the transaction, the recipient owes the debtor money
                if debtor_debt_after_transaction < 0:
                    # Since the debtor debt is negative, the recipient owes the debtor money.
                    # The debtor should no longer owe the recipient any money.
                    # Therefore, we will reset the debtor's debt to 0.
                    # And set the recipient debt to the absolute value of the debtor debt.
                    if debtor in debtor_dict:
                        debtor_dict[debtor][recipient] = 0

                    debtor_dict[recipient][debtor] = abs(
                        debtor_debt_after_transaction)

                # If after the transaction, the debtor still owes the recipient money
                elif debtor_debt_after_transaction > 0:
                    # If the debtor is not in the debtor_dict, add them
                    if debtor not in debtor_dict:
                        debtor_dict[debtor] = {
                            str(recipient): 0
                        }
                    if recipient in debtor_dict[debtor]:
                        # If the recipient is in the debtor's dictionary, add the amount to their debt.
                        debtor_dict[debtor][recipient] += debtor_debt_after_transaction
                    else:
                        # Set the debtor amount to debtor_debt_after_transaction
                        debtor_dict[debtor][recipient] = debtor_debt_after_transaction

                    # set the recipient amount to 0
                    debtor_dict[recipient][debtor] = 0
                else:
                    # After the the transaction, both the debtor and recipient owe each other 0.
                    # Therefore, we will set both to 0.
                    debtor_dict[recipient][debtor] = 0
                    if debtor in debtor_dict:
                        debtor_dict[debtor][recipient] = 0
                continue

        # If the debtor is not in the debtor_dict, add them
        # And set their debt to the amount.
        if debtor not in debtor_dict:
            debtor_dict[debtor] = {
                str(recipient): amount
            }
        # If the debtor is already in the debtor dict, add the amount to their debt.
        else:
            # If the debtor is not in the recipient's dictionary, add them
            # And set their debt to the amount.
            if recipient not in debtor_dict[debtor]:
                debtor_dict[debtor][recipient] = amount
            # If the debtor is already in the recipient's dictionary, add the amount to their debt.
            else:
                debtor_dict[debtor][recipient] += amount

    if (simplify):
        # Use our simplification algorithm to reduce the number of overall transactions.
        debtor_dict = simplify_debts(debtor_dict)

    # Set up an array of strings to store the output.
    output = []
    print("Debtor Dict: " + str(debtor_dict))
    # Iterate through the debtor_dict and print out the debts
    # in a readable format.
    for debtor in debtor_dict:
        for recipient in debtor_dict[debtor]:
            if debtor_dict[debtor][recipient] > 0:
                output.append(
                    f"{debtor} owes {recipient} ${debtor_dict[debtor][recipient]:.2f}")

    # If reset_tab is true, set all transactions in that group to paid.
    if (reset_tab):
        conn.execute(
            "UPDATE Transactions SET is_paid = 1 WHERE group_name = ?", (group_name,))
        conn.commit()
    conn.close()
    return output


def simplify_debts(debtor_dict):
    '''
    Simplifies the debts in the debtor_dict
    :param debtor_dict: 2-D Dictionary containing the debtor and the amount they owe each recipient.
    '''
    # Create a dictionary to store the absolute values.
    received_amounts = {}
    print(debtor_dict)
    for debtor in debtor_dict:
        for recipient in debtor_dict[debtor]:
            if debtor_dict[debtor][recipient] > 0:
                # If the debtor owes the recipient money
                # Subtract the owed amount from the debtor and add it to the recipient.
                if debtor not in received_amounts:
                    received_amounts[debtor] = 0
                if recipient not in received_amounts:
                    received_amounts[recipient] = 0
                received_amounts[debtor] -= debtor_dict[debtor][recipient]
                received_amounts[recipient] += debtor_dict[debtor][recipient]
    debtor_dict.clear()
    while (True):
        max_recipient = max(received_amounts.items(),
                            key=operator.itemgetter(1))[0]
        max_debtor = min(received_amounts.items(),
                         key=operator.itemgetter(1))[0]
        if round(received_amounts[max_recipient], 2) == 0.00:
            break
        if abs(received_amounts[max_debtor]) <= received_amounts[max_recipient]:
            if max_debtor in debtor_dict:
                debtor_dict[max_debtor][max_recipient] = abs(
                    received_amounts[max_debtor])
            else:
                debtor_dict[max_debtor] = {
                    max_recipient: abs(received_amounts[max_debtor])
                }
            received_amounts[max_recipient] += received_amounts[max_debtor]
            received_amounts[max_debtor] = 0
        else:
            if max_debtor in debtor_dict:
                debtor_dict[max_debtor][max_recipient] = received_amounts[max_recipient]
            else:
                debtor_dict[max_debtor] = {
                    max_recipient: received_amounts[max_recipient]
                }
            received_amounts[max_debtor] += received_amounts[max_recipient]
            received_amounts[max_recipient] = 0

    return debtor_dict


def validate_payload(payload):
    '''
    Validates the request payload to ensure values are correct.
    If a validation fails, we will raise an exception and pass it on to the caller.
    '''
    # Check that participant amounts add up to <= subtotal.
    sum = 0
    for participant in payload['participants']:
        amount = participant['amount']
        sum += amount if amount != None else 0
    if round(sum, 2) > payload['subtotal']:
        raise Exception(
            "Participant amounts add up to more than the subtotal.")


def audit_request(payload, status, audit_id, error_msg=None):
    '''
    Adds the request to the audit table.
    The schema for the audit table is as follows:
        id uuid not null primary key,
        transaction_id not null,
        request text not null,
        status text not null,
        error_msg text,
        timestamp datetime default current_timestamp
    We will first search for the transaction id in the audit table.
    If it exists, we will update the status and error_msg.
    If it does not exist, we will insert a new row.
    Then, we will return the audit id.
    '''
    print("Adding request to audit table with id: " + audit_id)
    conn = sqlite3.connect('database.db')
    conn.execute(
        "REPLACE INTO transaction_audit(id, transaction_id, request, status, error_msg) VALUES (?, ?, ?, ?, ?)",
        (audit_id, payload['id'], json.dumps(payload), status, error_msg))
    conn.commit()
    return audit_id
