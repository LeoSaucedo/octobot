import sqlite3
import uuid


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

    # Fill any missing values with default values
    if payload["tax"] is None:
        payload["tax"] = 0
    if payload["tip"] is None:
        payload["tip"] = 0
    if payload["ip"] is None:
        payload["ip"] = ""

    # Generate transaction ID
    transaction_id = str(uuid.uuid4())

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
        insert_transaction(transaction_id, payload["group"], payload["payer"],
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
        insert_transaction(transaction_id, payload["group"], payload["payer"],
                           even_split_participant["name"], even_split_amount, payload["memo"], payload["ip"])

    return transaction_id


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


def generate_report(group_name, reset_tab):
    '''
    Generates a report for the given group name.


    :param group_name: Name of the group to generate a report for
    :param reset_tab: Boolean indicating whether or not to reset the tab
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
    ip_addr text not null,
    memo text not null
    '''
    conn = sqlite3.connect('database.db')
    cursor = conn.execute(
        "SELECT * FROM Transactions WHERE group_name = ? and is_paid= ?", (group_name, 0))

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
                            str(recipient).lower(): 0
                        }
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
                str(recipient).lower(): amount
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
