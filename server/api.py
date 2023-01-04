from flask import Blueprint, request, render_template
import service

api = Blueprint('api', __name__)


@api.route('/api/health', methods=['GET'])
def health():
    '''
    This endpoint is used to check the health of the server.
    :return: OK
    '''
    return 'OK'


@api.route('/api/report/<group_name>', methods=['GET'])
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
    if len(report) == 0:
        return 'Group does not exist, or does not have any transactions', 404
    return report


@api.route('/api/transaction', methods=['POST'])
def transaction():
    '''
    This endpoint is used to add a transaction to a group.
    The json body of the request should be in the following format:
    {
    "group": "Nola",
    "payer": "Bryan",
    "subtotal": "100",
    "tax": "7",
    "tip": "20",
    "memo": "food",
    "debtors": [
        {
        "name": "Carlos",
        "amount": ""
        },
        {
        "name": "Jerm",
        "amount": "33"
        }
        ],
    "ip": "127.0.0.1"
    }

    :return: TransactionId of the transaction that was added
    '''
    data = request.get_json()
    if data is None:
        return 'Bad Request', 400
    return service.add_transaction(data)
