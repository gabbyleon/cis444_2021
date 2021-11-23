from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.logging import logger
from db_con import get_db_instance, get_db
import bcrypt

global_db_con = get_db()


def handle_request():
    logger.debug("Create Handle Request")
    cur = global_db_con.cursor()
    cur.execute("Select username from users where username = '"+ request.form['firstname']+ "';" )
    count = cur.fetchone()
    if count == None:
        salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
        decripSalt = salted.decode('utf-8')
        cur.execute(f"insert into users (username, password) values ('{request.form['firstname']}', '{decripSalt}');")
        print("User added!")
        global_db_con.commit()
        return "true"
    else:
        return "false"



