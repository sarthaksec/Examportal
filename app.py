from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///exam.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "clubtest"

class Passive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)   
    mail = db.Column(db.String(255), nullable=False)
    m_pass = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False) 
    roll = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer) 

    def __repr__(self) -> str:
        return f"{self.id} {self.name} {self.mail} {self.m_pass} {self.year} {self.roll} {self.marks}"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    que = db.Column(db.String(255), nullable=False)
    q_type = db.Column(db.String(50), nullable=False, default='mcq') # 'mcq', 'tf', 'fib'
    op1 = db.Column(db.String(255), nullable=True)  
    op2 = db.Column(db.String(255), nullable=True)  
    op3 = db.Column(db.String(255), nullable=True)  
    op4 = db.Column(db.String(255), nullable=True)  
    cans = db.Column(db.String(255), nullable=False)  
    year = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.que} {self.q_type} {self.cans}"

class Result(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_mail = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/login')
def login():
    return render_template('home.html')

@app.route('/passive-log', methods=['GET', 'POST'])
def passive_log():
    if request.method == 'POST':
        mail = request.form['mail']
        passw = request.form['pass']
        print(mail)
        print(passw)
        # if mail == "passive@gmail.com" and passw == "password":
        #     session["user"] = mail            
        #     return redirect(url_for('register'))
        # if mail == "admin@gmail.com" and passw == "admin123":
        #     return redirect(url_for('dashboard'))
        # else:
        #     return render_template('index.html')
        umail = Passive.query.filter_by(mail=mail).first()
        if umail:
            if passw==umail.m_pass:
                session["user"] = mail
                return redirect(url_for('student_dashboard'))
        return redirect(url_for('passive_log'))

@app.route('/', methods=['GET', 'POST'])
def register():        
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        m_pass = request.form['pass']        
        year = request.form['year']    
        roll = request.form['roll'] 
        marks = 0       
        stud = Passive(name=name, mail=mail, m_pass=m_pass, year=year, roll=roll, marks=marks)        
        db.session.add(stud)        
        db.session.commit()        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/addquestion', methods=['GET', 'POST'])
def dash():
    return render_template('addquestion.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    msg = None
    if request.method == 'POST':
        year = request.form.get('year')
        start = request.form.get('start_time')
        end = request.form.get('end_time')
        
        start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M')
        
        sched = Schedule.query.filter_by(year=year).first()
        if sched:
            sched.start_time = start_dt
            sched.end_time = end_dt
        else:
            sched = Schedule(year=year, start_time=start_dt, end_time=end_dt)
            db.session.add(sched)
        db.session.commit()
        msg = f"Schedule for {year} updated successfully!"
        
    return render_template('schedule.html', msg=msg)

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('results.html')    

@app.route('/addques', methods=['GET', 'POST'])
def addques():
    print("Entered in function")
    if request.method == 'POST':
        print("Entered in if")
        que = request.form.get('ques')
        q_type = request.form.get('q_type', 'mcq')
        op1 = request.form.get('op1')        
        op2 = request.form.get('op2')
        op3 = request.form.get('op3')
        op4 = request.form.get('op4')
        cans = request.form.get('cans')
        year = request.form.get('year')        
        ques = Question(que=que, q_type=q_type, op1=op1, op2=op2, op3=op3, op4=op4, cans=cans, year=year)
        db.session.add(ques)        
        db.session.commit()
        return render_template('addquestion.html')
        # return "Success"
    return render_template('dash.html')

@app.route('/exam', methods=['GET', 'POST'])
def exam():
    mail = session.get("user")
    if not mail:
        return redirect(url_for('login'))
    stud = Passive.query.filter_by(mail=mail).first()
    
    if not stud:
        session.pop("user", None)
        return redirect(url_for('register'))
    
    # Check Schedule
    sched = Schedule.query.filter_by(year=stud.year).first()
    now = datetime.now()
    if sched:
        if now < sched.start_time or now > sched.end_time:
            err = f"Exam for {stud.year} is not active. (Scheduled from {sched.start_time.strftime('%Y-%m-%d %H:%M')} to {sched.end_time.strftime('%Y-%m-%d %H:%M')})"
            return render_template('home.html', err=err)

    ques = Question.query.filter_by(year=stud.year)
    return render_template('exam.html', ques=ques)

@app.route('/student_dashboard')
def student_dashboard():
    mail = session.get("user")
    if not mail:
        return redirect(url_for('login'))
    history = Result.query.filter_by(student_mail=mail).order_by(Result.date.desc()).all()
    return render_template('student_dashboard.html', history=history)

@app.route('/certificate/<int:res_id>')
def certificate(res_id):
    mail = session.get("user")
    if not mail: return redirect(url_for('login'))
    res = Result.query.get(res_id)
    if not res or res.student_mail != mail:
        return "Unauthorized", 401
    stud = Passive.query.filter_by(mail=mail).first()
    if not stud:
        session.pop("user", None)
        return redirect(url_for('register'))
    return render_template('certificate.html', res=res, stud=stud)

@app.route('/allquestion', methods=['GET', 'POST'])
def allquestion():
    ques = Question.query.filter_by(year="SY")
    return render_template('allquestions.html', ques=ques)    

@app.route('/tyquestion', methods=['GET', 'POST'])
def tyquestion():
    ques = Question.query.filter_by(year="TY")
    return render_template('tyquestions.html', ques=ques)  


@app.route('/check', methods=['GET', 'POST'])
def check():
    result = 0
    mail = session.get("user")
    if not mail: return redirect(url_for('login'))
    stud = Passive.query.filter_by(mail=mail).first()
    if not stud:
        session.pop("user", None)
        return redirect(url_for('register'))
    
    # question = Question.query.all()
    question = Question.query.filter_by(year=stud.year)
    question_list = list(question)
    for quest in question_list:
        quest_id = str(quest.id)
        print("Question id : "+quest_id)
        select = request.form.get(quest_id, "").strip().lower()
        print("Selected id : "+ select)
        correct = quest.cans.strip().lower()
        if select == correct:
            result = result + 1
            print("correct")
        else:
            print("wrong")
    
    marks = result
    stud.marks = marks
    
    # Save into Result table for history
    res = Result(student_mail=mail, score=marks, total=len(question_list), date=datetime.now())
    db.session.add(res)
    
    db.session.add(stud)
    db.session.commit()
    
    marks = str(result)
    print(marks)
    return redirect(url_for('submit'))

@app.route('/submit')
def submit():
    mail = session.get("user")
    score = 0
    if mail:
        stud = Passive.query.filter_by(mail=mail).first()
        if stud:
            score = stud.marks
    return render_template('submit.html', score=score)

@app.route('/syresult', methods=['GET', 'POST'])
def syresult():
    res = Passive.query.filter_by(year="SY")
    return render_template('results.html', res=res) 

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
