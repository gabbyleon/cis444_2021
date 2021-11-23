from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.logging import logger
from db_con import get_db_instance, get_db
from datetime import date
global_db_con = get_db()


def handle_request():
    logger.debug("Complete Purchase Handle Request")
    cur = global_db_con.cursor()
    purcha = request.args.getlist("p[]")
   

    todaysdate= date.today()
    datestr = todaysdate.strftime('%m/%d/%Y')
    cur.execute("Select ID from users where username = '"+ g.jwt_data['sub'] + "';" )
    userID=cur.fetchone()

    for x in purcha:
        cur.execute("Select ID from books where bookname = '"+ x + "';" )
        bookID = cur.fetchone()
        cur.execute("Insert into purchases values(%s , %s , %s)",(userID[0] , bookID[0], datestr ))
        global_db_con.commit()


    return json_response( token = create_token(  g.jwt_data ))


