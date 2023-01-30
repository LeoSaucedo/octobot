from flask import Blueprint, request, render_template
import service
from flask_cors import cross_origin
import functools

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
    :return: The report for the group
    '''
    reset = request.args.get('reset', 'false')
    if reset not in ['true', 'false']:
        return 'Bad Request', 400
    report = service.generate_report(group_name, reset == 'true')
    return {"report": report}


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
    print("Incoming request with payload " + str(data), flush=True)
    if data is None:
        return 'Bad Request', 400
    transactionId = service.add_transaction(data)
    rows = service.get_db_rows(transactionId)
    print(rows)
    return rows
