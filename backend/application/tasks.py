import os
import csv
from sqlalchemy import engine
from application.workers import celery
from datetime import datetime
from celery.schedules import crontab
from jinja2 import Template
from flask import render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine
from application.utils import send_email
import re
from flask_sqlalchemy import session
from sqlalchemy.orm import Session
from datetime import datetime
from application.config import db_file
from application.models import Books, Sections, books_issued, Users,Requests,Ratings,sec_books
from flask import current_app as app
from flask import jsonify,request,make_response
from werkzeug.exceptions import HTTPException

engine =create_engine(db_file)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender,**kwargs):
     sender.add_periodic_task(
          crontab(hour=18, minute=15),
          send_daily_mail.s(),
     )
     sender.add_periodic_task(
          crontab(0, 0, day_of_month='1'),
          send_monthly_report.s(),
     )



@celery.task()
def send_daily_mail():
     template = """
     <p>
          Dear M/s. {{ name }},
     </p>
     <br />
     <p>
          We really miss you on our Library.
     </p>
     <p>
          Check out our latest Books.
     </p>
     <p>
          Excited to see you soon.
     </p>
     <br />
     <p>
          Best Regards,
     </p>
     <p>
          Library. 
     </p>
          
          """
     template = Template(template)
     with Session(engine) as session:
          current_date = datetime.now()
          formatted_date = current_date.strftime("%Y-%m-%d")
          userAll=session.query(Users).all()
          for i in userAll:
               if i.LoginTime==None or formatted_date != i.LoginTime:
                    print(f"user :${i.Name} not logined in today")
                    body= template.render(name=i.Name)
                    subject='Please Login Today'
                    send_email(i.Email,subject,body)
               else:
                    print(f"user :${i.Name} logined in today")
     return 200


@celery.task()
def send_monthly_report():

     adminEmail='rupaknalla1034@gmail.com'
     template='''

     <p>Dear Librarian,</p>
     <br>
     <h3>Monthly Report</h3>
     <br>
     {%if(booksCreated|length > 0)%}
          <h5>Books Created</h5>
          <table>
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Book Name</th>
                         <th>Author Name</th>
                         <th>AvgRating</th>
                         <th>Date Created</th>
                    </tr>
               </thead>
          
          {% for book in booksCreated %}
               <tbody>
                    <tr>
                    <td>{{ book.Bid }}</td>
                    <td>{{ book.Name }}</td>
                    <td>{{ book.AuthorName }}</td>
                    <td>{{ book.AvgRating }}</td>
                    <td>{{ book.CreatedDate }}</td>
                    </tr>
               </tbody>
          {% endfor %}
          </table>
     {% endif %}
     <br>
     {%if(sectionsCreated|length > 0)%}
          <h5>Sections Created</h5>
          <table>
               <thead>
                    <tr>
                         <th>SID</th>
                         <th>Section Name</th>
                         <th>Created Date</th>
                    </tr>
               </thead>
          
          {% for sec in sectionsCreated %}
               <tbody>
                    <tr>
                    <td>{{ sec.Sid }}</td>
                    <td>{{ sec.SName }}</td>
                    <td>{{ sec.CreatedDate}}</td>
                    </tr>
               </tbody>
          {% endfor %}
          </table>
     {% endif %}
     <br>
     {%if(booksIssuedCreated|length > 0)%}
          <h5>Books Issued</h5>
          <table>
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Book Name</th>
                         <th>Uid</th>
                         <th>user name</th>
                    </tr>
               </thead>
          
          {% for book in booksIssuedCreated %}
               <tbody>
                    <tr>
                    <td>{{ book.Bid }}</td>
                    <td>{{ book.BName }}</td>
                    <td>{{ book.Uid }}</td>
                    <td>{{ book.UName }}</td>
                    </tr>
               </tbody>
          {% endfor %}
          </table>
     {% endif%}
     <br>
     {% if(booksRatingCreated|length > 0)%}
          <h5>Books Ratings</h5>
          <table>
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Book Name</th>
                         <th>Uid</th>
                         <th>User Name</th>
                         <th>Rating</th>
                    </tr>
               </thead>
          
          {% for book in booksRatingCreated %}
               <tbody>
                    <tr>
                    <td>{{ book.Bid }}</td>
                    <td>{{ book.BName }}</td>
                    <td>{{ book.Uid }}</td>
                    <td>{{ book.UName }}</td>
                    <td>{{ book.rating }}</td>
                    </tr>
               </tbody>
          {% endfor %}
          </table>
     {% endif %}
     '''
     template = Template(template)
     current_date = datetime.now()
     formatted_date = current_date.strftime("%Y-%m-%d")
     with Session(engine) as session:
          # books created
          booksAll=session.query(Books).all()
          booksCreated=[]
          for i in booksAll:
               if(int(i.CreatedDate[5:7])==int(formatted_date[5:7])):
                    booksCreated.append(i)
          
          # sections created
          secCreated=[]
          secs=session.query(Sections).all()
          for i in secs:
               if(int(i.CreatedDate[5:7])==int(formatted_date[5:7])):
                    secCreated.append(i)
          
          # books issued
          booksIssues=[]
          booksIssuesAll=session.query(books_issued).all()
          for i in booksIssuesAll:
               if(int(i.DateOfIssued[5:7])==int(formatted_date[5:7])):
                    user=session.query(Users).filter(Users.id==i.Uid).first()
                    book=session.query(Books).filter(Books.Bid==i.Bid).first()
                    booksIssues.append({
                         'Bid':i.Bid,
                         'BName':book.Name,
                         'Uid':user.id,
                         'UName':user.Name
                    })
          
          # booksRatingCreated
          booksRatings=[]
          bookRates=session.query(Ratings).all()
          for i in bookRates:
               if (int(i.CreatedDate[5:7])==int(formatted_date[5:7])):
                    user=session.query(Users).filter(Users.id==i.Uid).first()
                    book=session.query(Books).filter(Books.Bid==i.Bid).first()
                    temp={
                         'Uid':user.id,
                         'UName':user.Name,
                         'Bid':book.Bid,
                         'BName':book.Name,
                         'rating':i.Rating
                    }
                    booksRatings.append(temp)
          body= template.render(booksRatingCreated=booksRatings,booksIssuedCreated=booksIssues,sectionsCreated=secCreated,booksCreated=booksCreated)
          print(booksCreated)
          # body=template.render(booksCreated=booksCreated)
          subject='Monthly Report'
          send_email(adminEmail,subject,body)
     return 200


# export csv file
@celery.task()
def csv_report():
     print()
     
     adminEmail='rupaknalla1034@gmail.com'
     report_filename = "books_issued_report.csv"
     date = datetime.now().date()
     timestamp = datetime.now().strftime("%a %b %d %Y %I:%M:%S %p")
     if os.path.exists(report_filename):
          os.remove(report_filename)
     with open(report_filename, "w", newline='') as f:
          f = csv.writer(f, delimiter=',')
          f.writerow(["","","BOOKS ISSUED AND NOT RETURNED","",""])
          f.writerow(["Bid","book name","Uid","username","date of issue"])
          with Session(engine) as session:
               booksIssuesAll=session.query(books_issued).all()
               for i in booksIssuesAll:
                    
                         user=session.query(Users).filter(Users.id==i.Uid).first()
                         book=session.query(Books).filter(Books.Bid==i.Bid).first()
                         f.writerow([i.Bid,book.Name,user.id,user.Name,i.DateOfIssued])
     template_str = """
          <p>
               Dear Admin,
          </p>
          <br />
          <p>please find the below attched csv file for list of books and users who have not retured their book yet</p>
               Best regards,
          <br />
               Library
          </p>
          """
     template = Template(template_str)
     file = open(report_filename, "rb")
     subject='book issues report'
     body=template.render()
     send_email(adminEmail, subject, body, attachment=file, filename=report_filename, subtype="csv")
     file.close()
     os.remove(report_filename)