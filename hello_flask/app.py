from flask import Flask,render_template,request, redirect, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from db_con import get_db_instance, get_db
import json
import jwt
import bcrypt
import datetime as dt

app = Flask(__name__)
FlaskJSON(app)
app.secret_key = "hello"
USER_PASSWORDS = { "cjardin": "strong password"}

globaltoken = None
bookp = {"order" : []
        }

CUR_ENV = "PRD"
JWT_SECRET = "4prez"
global_db_con = get_db()

#@app.route('/') #endpoint
#def index():
#   return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']


@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now()) } )

@app.route('/backp')#, methods=['POST']) #endpoint
def backp():
    cur = global_db_con.cursor()
    #salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    cur.execute("insert into users values ('cheeks', 'hello');")
    global_db_con.commit()
    return json_response(status="good")


#Assignment 3-------------------------------------------------------------------------
def checkToken(token):
    if globaltoken is None:
        print("No token has been saved")
        return False
    else: 
        global_tokenc = jwt.decode(globaltoken, JWT_SECRET, algorithms = ["HS256"])
        user_token =  jwt.decode(token, JWT_SECRET, algorithms = ["HS256"])
        
        if global_tokenc == user_token:
            print("Accepted Token..")
            true = "True"
            return true
        else:
            print("Invalid Token...")
            return "False" 


@app.route('/hellodb', methods=['POST']) #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("Select username from users where username = '"+ request.form['username']+ "';" )
    count = cur.fetchone()
    if count == None:
        salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
        decripSalt = salted.decode('utf-8')
        print(decripSalt)
        cur.execute(f"insert into users (username, password) values ('{request.form['username']}', '{decripSalt}');")
        global_db_con.commit()
        return "true"
    else:
        return "false"


@app.route('/account', methods=['POST','GET']) #endpoint
def account():
    cur = global_db_con.cursor()
    cur.execute(f"Select password from users where username = '{ request.form['username']}';" )
    getpassword=cur.fetchone()[0]
    if bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), bytes(getpassword, 'utf-8')):
        global globaltoken 
        globaltoken = jwt.encode({"username": request.form['username'],
                                  "password": request.form['password']},
                                   JWT_SECRET, algorithm="HS256") 
        check = {"pass" : "pass",
                 "jwt"  : "" +globaltoken+"",
                 "booklist":[],
                 "price": []};
        return getbooks(check)
    else: 
        check = {"pass" : "fail"}
        return  json.dumps(check)

@app.route('/getbooks', methods=["GET"]) #endpoint
def getbooks(check):
    cur = global_db_con.cursor()
    cur.execute("Select bookname from books;" )
    count=cur.fetchall()
    cur.execute("Select price from books;" )
    cost=cur.fetchall()
    
    for row in count: 
        check["booklist"].append(row)
    for row in cost: 
        check["price"].append(row)

    return json.dumps(check)

@app.route('/purchaseBook', methods=["POST"]) #endpoint
def purchaseBook():
    clear = checkToken(request.form['sessionJWT'])
    true = "True"
    if clear == true:
      result = jwt.decode(globaltoken, JWT_SECRET, algorithms = ["HS256"])
      bookp["order"].append(request.form['bookname'])
      return json_response(status="good")  
    else:
       print("JWT Failed") 
       return json_response(status="error")
 
@app.route('/completeOrder', methods=["POST","GET"]) #endpoint
def completeOrder():
        clear = checkToken(request.form['sessionJWT'])
        true = "True"
        if clear == true:
          cur = global_db_con.cursor()
          result = jwt.decode(globaltoken, JWT_SECRET, algorithms = ["HS256"])
          todaysdate= dt.date.today();
          cur.execute("Select ID from users where username = '"+ result['username']+ "';" )
          userID=cur.fetchone()

          for x in bookp['order']:
              cur.execute("Select ID from books where bookname = '"+ x + "';" )
              bookID = cur.fetchone()
              cur.execute("Insert into purchases values(%s , %s , %s)",(userID[0] , bookID[0], todaysdate )) 
              global_db_con.commit()
              return json.dumps(bookp)
        else:
            print("JWT Failed")
            return json_response(status="error")


#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/s2') #endpoint
def s2():
    return render_template('backatu.html') 




###########Final###########
@app.route('/s9') #endpoint
def s9():
    return redirect('/static/test.html')

@app.route('/insertpic' , methods=["POST","GET"]) #endpoint
def insertpic():
    cur = global_db_con.cursor()
    cur.execute("INSERT into userspictures(userid, picurl)  values (121 ,'"+ request.form['url']+ "') ;")

    global_db_con.commit()
    return json_response(status="good")

@app.route('/getpics' , methods=["POST","GET"]) #endpoint
def getpics():
    cur = global_db_con.cursor()
    cur.execute("Select picurl from userspictures where userid = " +request.form['user']+ "  ;")
    count = cur.fetchall()
    data = {"link" : []};
    for row in count:
        data["link"].append(row)
    return json.dumps(data)

app.run(host='0.0.0.0', port=80)

