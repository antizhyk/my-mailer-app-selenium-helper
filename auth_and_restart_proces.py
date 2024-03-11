import requests
from flask import Response

from auth import auth


def auth_and_restart_proces(account_id):
    try:
        result = auth(account_id)
        print("===============result:", result)
        if "Error authenticating" in result:
            return Response(status=500, response="Error authenticating? please check your credentials and user-agent "
                                                 "and try again or contact support")
        res = requests.get(f'http://localhost:5000/start/{account_id}')
        print("===============response:", res.status_code, res.text)
        return Response(status=200, response="Re-auth and restart process successfully")
    except Exception as e:
        print("Error reauth:", str(e))
        raise e