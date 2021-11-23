from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.logging import logger
from db_con import get_db_instance, get_db
import bcrypt

global_db_con = get_db()




def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    
    cur = global_db_con.cursor()
    cur.execute(f"Select password from users where username = '{ request.form['firstname']}';" )
    getpassword=cur.fetchone()[0]
    if bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), bytes(getpassword, 'utf-8')):
        user = {
              "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
               }
        return json_response( token = create_token(user) , authenticated = True)
    else:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

