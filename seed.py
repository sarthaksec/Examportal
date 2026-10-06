import sys
from datetime import datetime, timedelta
sys.path.append('.')
from app import db, app, Schedule, Question

app.app_context().push()

# 1. Add Schedule for SY
# Let's make it from yesterday to tomorrow so it's definitely active
now = datetime.now()
start = now - timedelta(days=1)
end = now + timedelta(days=1)

# clear existing schedules to be safe
Schedule.query.delete()

sched_sy = Schedule(year='SY', start_time=start, end_time=end)
db.session.add(sched_sy)

# 2. Add Questions for SY
# Clear existing questions for SY
Question.query.filter_by(year='SY').delete()

# Question 1: MCQ
q1 = Question(
    que="What does HTML stand for?",
    q_type="mcq",
    op1="Hyper Text Markup Language",
    op2="High Text Machine Language",
    op3="Hyper Tabular Markup Language",
    op4="None of these",
    cans="1",
    year="SY"
)

# Question 2: True/False
q2 = Question(
    que="Python is a compiled language.",
    q_type="tf",
    op1=None, op2=None, op3=None, op4=None,
    cans="false",
    year="SY"
)

# Question 3: Fill in the Blanks
q3 = Question(
    que="Flask is a web framework written in ____.",
    q_type="fib",
    op1=None, op2=None, op3=None, op4=None,
    cans="python",
    year="SY"
)

# Question 4: MCQ
q4 = Question(
    que="Which of the following is used to style web pages?",
    q_type="mcq",
    op1="HTML",
    op2="JQuery",
    op3="CSS",
    op4="XML",
    cans="3",
    year="SY"
)

# Question 5: True/False
q5 = Question(
    que="SQLAlchemy is an Object Relational Mapper (ORM).",
    q_type="tf",
    op1=None, op2=None, op3=None, op4=None,
    cans="true",
    year="SY"
)

db.session.add_all([q1, q2, q3, q4, q5])
db.session.commit()
print("Database seeded with a sample test and active schedule for 'SY'.")
