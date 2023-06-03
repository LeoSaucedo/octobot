from flask import Blueprint, request, render_template
import service
from flask_cors import cross_origin
import functools
import traceback

print = functools.partial(print, flush=True)

api = Blueprint('api', __name__)


@api.route('/api/health', methods=['GET'])
def health():
    '''
    This endpoint is used to check the health of the server.
    :return: OK
    '''
    return 'OK'


@api.route('/api/report/<group_name>', methods=['GET'])
@cross_origin()
def report(group_name):
    '''
    This endpoint is used to get the report for a group.
    :param group_name: A url parameter representing the name of the group to get the report for
    :query reset: If true, the report will be reset after it is returned
    :query simplify: If true, the report will be simplified
    :return: The report for the group
    '''
    reset = request.args.get('reset', 'false')
    simplify = request.args.get('simplify', 'false')
    print("Incoming request for report for group: " +
          str(group_name) + " with reset: " + str(reset)
          + " and simplify: " + str(simplify))
    if reset not in ['true', 'false']:
        return 'Bad Request', 400
    report = service.generate_report(
        group_name, reset == 'true', simplify == 'true')
    transactions = service.get_transactions(group_name)
    return {"report": report, "transactions": transactions}


@api.route('/api/transaction/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    '''
    This endpoint is used to delete a transaction from a group.
    Upon success, we will return 204 NO_CONTENT.
    :param transaction_id: A url parameter representing the id of the transaction to delete
    :return: NO_CONTENT
    '''
    print("Incoming request to delete transaction: " + str(transaction_id))
    service.delete_transaction(transaction_id)
    return 'successfully deleted transaction ' + str(transaction_id), 200


@api.route('/api/transaction', methods=['POST'])
def transaction():
    '''
    This endpoint is used to add a transaction to a group.
    The json body of the request should be in the following format:
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

    :return: TransactionId of the transaction that was added
    '''
    data = request.get_json()
    response = None
    print("Incoming request with payload: " + str(data))
    if data is None:
        response = 'Bad Request', 400
    try:
        transactionId = service.add_transaction(data)
    except Exception as e:
        # Print error with stack trace
        print(traceback.format_exc())
        return str(e), 400
    rows = service.get_db_rows(transactionId)
    print("Response content: " + str(rows))
    return rows
