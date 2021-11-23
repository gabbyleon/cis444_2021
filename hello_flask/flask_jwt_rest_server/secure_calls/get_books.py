from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.logging import logger
from db_con import get_db_instance, get_db
global_db_con = get_db()


def handle_request():
    logger.debug("Get Books Handle Request")
    cur = global_db_con.cursor()
    cur.execute("Select bookname, price from books;" )
    count=cur.fetchall()
    booklists = []
    for row in count: 
        booklists += row
    return json_response( token = create_token(  g.jwt_data ) , books=booklists)

