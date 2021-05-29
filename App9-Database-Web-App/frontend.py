from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename

database_heroku = "postgres://lrautwfgwkcmof:a0af3a6f380abc2aa8dcde131a456c67deac25e28ffe2ffa692dba6f5a656746@ec2-3-215-207-12.compute-1.amazonaws.com:5432/d1vbuet7m26ih9"
# add ssl to be able usein command line
database_heroku = database_heroku+"?sslmode=require"
database_user = 'postgresql://postgres:postgres123@localhost/height_collector'

app = Flask(__name__)
#config link to database postgresql
app.config['SQLALCHEMY_DATABASE_URI']=database_heroku
db = SQLAlchemy(app)

class Data(db.Model):
    #table name
    __tablename__ = "data"
    # create ID first. type is Integer
    id = db.Column(db.Integer, primary_key=True)
    #create column for email with 120 charater long and unique (no same email)
    email_ = db.Column(db.String(120), unique=True)
    #create column for height, type is integer
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_= email_
        self.height_ = height_

@app.route('/')
def index():
    return render_template("index.html", btn="")

# add method for action="{{url_for('success')}}" work in (index.html)
@app.route('/success', methods=["POST"])
def success():
    if request.method == "POST" :
        email = request.form["email_name"]
        height = request.form["height_name"]
        #check if email is duplicate
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            # add to database
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            # cal average height
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            #cal how many user
            count = db.session.query(Data.height_).count()
            #send email
            send_email(email, height, average_height, count)
            return render_template("success.html")
    return render_template("index.html",
    text="Seems like we've got something from that email address already")

@app.route('/loadfile', methods=["POST"])
def loadfile():
    global file
    if request.method == "POST" :
        file = request.files["file"]
        #content = file.read()
        # use secure_filename to ignore slash=> keep secure from hacker
        file.save(secure_filename("uploaded"+file.filename))
        
        with open("uploaded"+file.filename,"a") as f:
            f.write("This was added later")
        return render_template("index.html", btn="download.html")

@app.route('/download')
def download() :
    #as_attachment = True to download file, not open in browser
    return send_file("uploaded"+file.filename, attachment_filename="yourfile.csv", as_attachment=True)

if __name__=="__main__":
    app.debug = True
    #if want port 5001 =>app.run(port=5001). Default is 5000
    app.run()
