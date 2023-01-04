from flask import Flask, request, render_template
import service
import sqlite3
import api
import os

app = Flask(__name__)

<<<<<<< HEAD
=======
app.register_blueprint(api.api)
>>>>>>> 498001242923836eb35c39cf2455c86b3f05b76a

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    if request.method == "POST":
        formResponse = request.form.to_dict(flat=False)
        payload = {}
        payload["group"] = formResponse["group"][0].lower().strip()
        payload["payer"] = formResponse["payer"][0].lower().strip()
        payload["subtotal"] = formResponse["subtotal"][0]
        payload["tax"] = formResponse["tax"][0]
        payload["tip"] = formResponse["tip"][0]
        payload["memo"] = formResponse["memo"][0].lower().strip()
        participants = []
        for i in range(len(formResponse["names"])):
            participant = {}
            participant["name"] = formResponse["names"][i].lower().strip()
            participant["amount"] = formResponse["amounts"][i]
            participants.append(participant)
        payload["participants"] = participants
        # Add user's IP to payload
        payload["ip"] = request.remote_addr
        transactionId = service.add_transaction(payload)
        # Connect to the database and retrieve all values for the given transactionId.
        conn = sqlite3.connect('database.db')
        cursor = conn.execute(
            "SELECT * FROM Transactions WHERE transaction_id = ?", (transactionId,))
        rows = cursor.fetchall()
        conn.close()
        print(payload)
        return render_template("confirmation.html", payload=payload, calculations=str(rows), transactionId=transactionId)
    return render_template("transaction.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        return render_template("report-page.html", report=service.generate_report(request.form["group"].lower().strip(), request.form.__contains__("reset")))
    return render_template("report.html")


if __name__ == "__main__":
    app.run("0.0.0.0")
