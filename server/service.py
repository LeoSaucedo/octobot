import sqlite3
import uuid



def add_transaction(payload):
    # Insert payload values into the database
    # Calculate the amount by adding tax and tip to the subtotal
    transactionId = str(uuid.uuid4())
    payerInParticipants = False
    for participant in payload["participants"]:
        if (participant["name"] == payload["payer"]):
            payerInParticipants = True
            break
    if (payerInParticipants == False):
        participant = {
            "name": payload["payer"],
            "amount": ""
        }
        payload["participants"].append(participant)

    amount = None
    splitters = []
    rats = []
    for participant in payload["participants"]:
        if participant['amount'] == "":
            splitters.append(participant)
        else:
            rats.append(participant)

    tax_percent = float(payload["tax"]) / float(payload["subtotal"])
    tip_percent = float(payload["tip"]) / float(payload["subtotal"])

    totalRatAmount = 0

    for rat in rats:
        amount = float(rat["amount"])+(float(rat["amount"])*tax_percent)+(float(rat["amount"])*tip_percent)
        totalRatAmount += amount
        if rat["name"] == payload["payer"]:
            continue
        insert_transaction(transactionId, payload["group"], payload["payer"], rat["name"], amount, payload["ip"],payload["memo"])

    if len(splitters) > 0:
        splitterAmount = ((float(payload["subtotal"]) + float(payload["tax"]) + float(payload["tip"])) - totalRatAmount ) / len(splitters)
    for splitter in splitters:
        if splitter["name"] == payload["payer"]:
            continue
        insert_transaction(transactionId, payload["group"], payload["payer"], splitter["name"], splitterAmount, payload["ip"],payload["memo"])
    return transactionId
    

def insert_transaction(transactionId, groupName, purchaser, debtor, amount,ipAddress, memo):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO Transactions(id,transaction_id,group_name,purchaser,debtor,amount,is_paid,ip_addr,memo) VALUES (?,?,?,?,?,?,?,?,?)",
    (str(uuid.uuid4()),transactionId, groupName, purchaser, debtor, amount, 0, ipAddress,memo))
    conn.commit()
    conn.close()

def generate_report(groupName, resetTab):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM Transactions WHERE group_name = ? and is_paid= ?", (groupName,0))
    punnett = {}
    for payment in cursor.fetchall():
        debtor = payment[4]
        recipient = payment[3]
        amount = payment[5]
        if recipient in punnett:
            if debtor in punnett[recipient]:
                recipientDebt = punnett[recipient][debtor]
                recipientDebtAfterTransaction = amount - recipientDebt
                if recipientDebtAfterTransaction < 0:
                    #set debtor amount to 0
                    if debtor in punnett:
                        punnett[debtor][recipient] = 0
                    #set the recipient debt to abs(recipientDebtAfterTransaction)
                    punnett[recipient][debtor] = abs(recipientDebtAfterTransaction)
                elif recipientDebtAfterTransaction > 0:
                    #set the debtor amount to recipentDebtAfterTransaction
                    if debtor not in punnett:
                        punnett[debtor] = {
                            str(recipient).lower(): 0
                        }
                    if recipient in punnett[debtor]:
                        punnett[debtor][recipient] += recipientDebtAfterTransaction
                    else:
                        punnett[debtor][recipient] = recipientDebtAfterTransaction
                    #set the recipient amount to 0
                    punnett[recipient][debtor] = 0
                else:
                    #set both to 0
                    punnett[recipient][debtor] = 0
                    if debtor in punnett:
                        punnett[debtor][recipient] = 0
                continue
                
        if debtor not in punnett:
            punnett[debtor] = {
                str(recipient).lower(): amount
            }
        else:
            if recipient not in punnett[debtor]:
                punnett[debtor][recipient] = amount
            else:
                punnett[debtor][recipient] += amount

    output = []
    for debtor in punnett:
        for recipient in punnett[debtor]:
            if punnett[debtor][recipient] > 0:
                output.append(debtor + " owes " + recipient + " $" + str(round(punnett[debtor][recipient], 2)))
    
    if (resetTab):
        conn.execute("UPDATE Transactions SET is_paid = 1 WHERE group_name = ?", (groupName,))
        conn.commit()
    conn.close()
    return {'report': output}
