from flask import Flask

from auth import auth
from auth_and_restart_proces import auth_and_restart_proces
from get_chats import get_chats
from get_messages import get_messages
from selenium_logic import test_driver

app = Flask(__name__)


def hello_world():
    return "<p>Hello, World!</p>"


app.add_url_rule('/', 'index', hello_world)
app.add_url_rule('/test', 'test', test_driver)
app.add_url_rule('/get_chats/<account_id>', 'get_chats', get_chats)
app.add_url_rule('/auth/<account_id>', 'auth', auth)
app.add_url_rule('/auth_and_restart_proces/<account_id>', 'auth_and_restart_proces', auth_and_restart_proces)

app.add_url_rule('/get-messages/<account_id>', 'get-messages', get_messages)

#
# @app.route('/auth_and_restart_proces/<account_id>', methods=['GET'])
# def auth_and_restart_proces_route(account_id):
#     return auth_and_restart_proces(account_id)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
