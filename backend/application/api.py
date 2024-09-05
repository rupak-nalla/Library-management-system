import re
from flask_sqlalchemy import session
from sqlalchemy import create_engine
from flask_restful import Resource,Api, marshal_with,fields
from sqlalchemy.orm import Session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import os
from application.config import db_file
from application.models import Books, Sections, books_issued, Users,Requests,Ratings,sec_books
from flask import current_app as app
from flask import jsonify,request,make_response
from werkzeug.exceptions import HTTPException
from datetime import datetime
from application.cache import cache
from application.tasks import csv_report
api=Api()
engine =create_engine(db_file)
token_field={
     "token":fields.String
}

class ExistsError(HTTPException):  #409

  def __init__(self,msg):
    self.response = make_response(msg, 409)

class NotFoundError(HTTPException):  #404

  def __init__(self,msg):
    self.response = make_response(msg, 404)

class BussinessValidationError(HTTPException):  
  def __init__(self,msg):
    self.response = make_response(msg, 422)


class UserLoginAPI(Resource):
     
     @marshal_with(token_field)
     def post(self):
          userFound=False
          token=''
          with Session(engine) as session:
               
               uname=request.json.get('username',None)
               password=request.json.get('password',None)
               user=session.query(Users).filter(Users.Name==uname,Users.Password==password).first()
               if(user):
                    userFound=True
                    token=create_access_token(identity=user.id)
                    
                    current_date = datetime.now()
                    formatted_date = current_date.strftime("%Y-%m-%d")  # Change format as needed
                    print("Formatted current date:", formatted_date)
                    user.LoginTime=formatted_date
                    session.commit()
                    
               else:
                    return 404,"user not found"
          if userFound:
               return {"token":token},200
api.add_resource(UserLoginAPI,"/api/UserLogin")

class UserRegistrationAPI(Resource):
     def post(self):
          try:
               un=request.json.get('username')
               pw=request.json.get('password')
               email=request.json.get('Email')
               with Session(engine) as session:
                    user=session.query(Users).filter(Users.Name==un).first()
                    if(user):
                         raise ExistsError(msg="username exists",status_code=409)
                    newUser=Users(Name=un,Password=pw,Email=email)
                    session.add(newUser)
                    session.commit()
                    return 200,{"message":"User Added"}
          except ExistsError as ee:
               raise ee
api.add_resource(UserRegistrationAPI,"/api/Register")


user_details={
     "id":fields.Integer,
     "Name":fields.String,
     "Email":fields.String,
     "BCount":fields.Integer,
     "ProfileImg":fields.String
}
assets= os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src','assets','Images'))
class UserDetails(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self):
          try:
               current_user = get_jwt_identity()
               if( not current_user):
                    raise NotFoundError(msg="User Not Found")
               with Session(engine) as session:
                    user=session.query(Users).filter(Users.id==current_user).first()
                    # mybooks=session.query(books_issued).filter(books_issued.Uid==user.id).all()
                    # mybook_ids = [mybook.bookId for mybook in mybooks]
                    # booksAll=session.query(Books).filter(~Books.id.in_(mybook_ids)).all()
                    # mybooks_json=[]
                    # booksAll_json=[]
                    # mybooksDetails=session.query(Books).filter(Books.Bid.in_(mybook_ids)).all()
                    # for i in range(len(mybooks)):
                    #      temp={
                    #           "name":mybooksDetails[i].Name,
                    #           "AuthorName":mybooksDetails[i].AuthorName,
                    #           "Rating":mybooksDetails[i].AvgRating
                    #      }
                    if(user.ProfileImg):
                         return {"id":user.id,"Name":user.Name,"Email":user.Email,"ProfileImg":user.ProfileImg}
                    else:
                         return {"id":user.id,"Name":user.Name,"Email":user.Email}

          except NotFoundError as nfe:
               raise nfe
          except Exception as e:
               raise e
     @jwt_required()
     def put(self):
          try:
               current_user=get_jwt_identity()
               print(current_user)
               username = request.form['editUserName']
               email = request.form['editEmail']
               print(f"username:${username}\n email:${email}")
               with Session(engine) as session:
                    
                    filePresent=True
                    if 'file' not in request.files:
                         filePresent=False
                    
                    user=session.query(Users).filter(Users.id==current_user).first()
                    userDup=session.query(Users).filter(Users.Name==username,Users.id!=user.id).first()
                    if(userDup):
                         raise ExistsError(status_code=409,msg="user name already exists")
                    if(not user):
                         raise NotFoundError(msg="user not found")
                    user.Name=username
                    user.Email=email
                    if(filePresent):
                         file = request.files['file']
                         if file.filename == '':
                              return {'message': 'No file selected for uploading'}, 400
                         filename="profile_"+str(current_user)+".jpg"
                         
                         file_path = os.path.join(assets, filename)
                         file.save(file_path)
                         user.ProfileImg=file_path
                    cache.clear()
                    session.commit()
               return 200
          except ExistsError as ee:
               raise ee
          except NotFoundError as nfe:
               raise nfe
          except Exception as e:
               raise e
api.add_resource(UserDetails,"/api/user")


class Librarian(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self):
          uid=get_jwt_identity()
          if(not uid==0):
               return {'msg':'only for librarian'},401
          data={
               'Bcount':0,
               'BIcount':0,
               'SecCount':0,
               'Reqs':[]
          }
          with Session(engine) as session:
               req=session.query(Requests).all()
               
               data["Bcount"]=session.query(Books).count()
               data["BIcount"]=session.query(books_issued).count()
               booksAll=session.query(Books).all()
               data['SecCount']=session.query(Sections).count()
               for i in req:
                    user=session.query(Users).filter(Users.id==i.Uid).first()
                    Book=session.query(Books).filter(Books.Bid==i.Bid).first()
                    data["Reqs"].append({
                         "Bid":i.Bid,
                         "BookName":Book.Name,
                         "UName":user.Name,
                         "Uid":user.id,
                         "Bcount":user.BCount,
                         "Status":i.Status
                    })
               
               return data,200
     
     def post(self):
          try:
               username=request.json.get("username")
               password=request.json.get("password")
               if(username=="Lib@123" and password =="Password@1"):
                    token=create_access_token(identity=0)

                    return {"token":token},200
               else:
                    raise NotFoundError(msg="Incorrect username/password")
          except NotFoundError as nfe:
               raise nfe
          except Exception as e:
               raise e
api.add_resource(Librarian,'/api/Librarian')

class BooksRes(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self):
          try:
               with Session(engine) as session:
                    booksAll=session.query(Books).all()
                    if(not booksAll):
                         raise NotFoundError(msg="Books Not Found")
                    book_list = [book.to_dict() for book in booksAll]
                    return book_list,200
          except NotFoundError as nfe:
               raise nfe
          except Exception as e:
               raise e
     
     @jwt_required()
     def post(self):
          try:
               uid = get_jwt_identity()
               if uid != 0:
                    return {"msg": "You're not a Librarian"}, 422
               bookName = request.form['BookName']
               authorName = request.form['AuthorName']
               file = request.files['file']
               Content=request.form['Content']
               with Session(engine) as session:
                    bookDup = session.query(Books).filter(Books.Name == bookName).first()
                    if bookDup:
                         raise ExistsError(msg="Book Name is already in use")
                    if file.filename == '':
                         return {'message': 'No file selected for uploading'}, 400
                    filename = f"{bookName}.jpg"
                    file_path = os.path.join(assets, filename)
                    current_date = datetime.now()
                    formatted_date = current_date.strftime("%Y-%m-%d")  # Change format as needed
                    print("Formatted current date:", formatted_date)
                    newBook = Books(Name=bookName, AuthorName=authorName, CoverPath=file_path,CreatedDate=formatted_date,Content=Content)
                    session.add(newBook)
                    file.save(file_path)
                    session.commit()
               cache.clear()
               return {"msg": "Book Created successfully"}, 200
          except ExistsError as ee:
               raise ee


          # if file.filename == '':
          #      return {'message': 'No file selected for uploading'}, 400
          # filename="profile_"+str(current_user)+".jpg"
          
          # file_path = os.path.join(assets, filename)
          # file.save(file_path)
          # user.ProfileImg=file_path

     @jwt_required()
     def put(self):
          try:
               bid=request.form['Bid']
               bname=request.form['BookName']
               author=request.form['AuthorName']
               Content=request.form['Content']
               with Session(engine) as session:
                    book=session.query(Books).filter(Books.Bid==bid).first()
                    print(book.to_dict())
                    if(not book):
                         raise NotFoundError(msg="Book Not Found")
                    bookDup=session.query(Books).filter(Books.Name==bname,Books.Bid!=bid).first()
                    if(bookDup):
                         raise ExistsError(msg="book name is already in use")
                    book.Name=bname
                    book.AuthorName=author
                    book.Content=Content
                    print(f"book:${bname};author:${author}")
                    if('file' in request.files):
                         file = request.files['file']
                         filename = f"{bname}.jpg"
                         file_path = os.path.join(assets, filename)
                         book.CoverPath=file_path
                         file.save(file_path)
                    session.commit()
               with Session(engine) as session :
                    book=session.query(Books).filter(Books.Bid==bid).first()
                    print(book.to_dict())
               cache.clear()
               return {"msg":"modified successfully"},200
          except NotFoundError as nfe:
               raise nfe
          except ExistsError as ee:
               raise ee

     @jwt_required()
     def delete(self):
          try:
               uid=get_jwt_identity()
               if(not uid==0):
                    return {"msg":"Your not Librarian"},409
               bid=request.json.get("Bid")
               with Session(engine) as session:
                    book = session.query(Books).filter(Books.Bid==bid).first()
                    if not book:
                         raise NotFoundError(msg="Book Not Found")
                    book_issues=session.query(books_issued).filter(books_issued.Bid==bid).all()
                    if(book_issues):
                         
                         for i in book_issues:
                              session.delete(i)
                    book_reqs=session.query(Requests).filter(Requests.Bid==bid).all()
                    if(book_reqs):
                         for i in book_reqs:
                              session.delete(i)
                    book_ratings=session.query(Ratings).filter(Ratings.Bid==bid).all()
                    if book_ratings :
                         for i in book_ratings:
                              session.delete(i)
                    book_sec=session.query(sec_books).filter(sec_books.Bid==bid).all()
                    if(book_sec):
                         for i in book_sec:
                              session.delete(i)
                    session.delete(book)
                    cache.clear()
                    session.commit()
               return {"msg":"Deleted Successfully"},200
          except NotFoundError as nfe:
               raise nfe

api.add_resource(BooksRes,"/api/books")
class BookReq(Resource):
     @jwt_required()
     def post(self):
          try:
               userid=get_jwt_identity()
               Bid=request.json.get('Bid')
               with Session(engine) as session:
                    user=session.query(Users).filter(Users.id==userid).first()
                    if(not user):
                         raise NotFoundError(msg="user not found")
                    uname=user.Name
                    Book=session.query(Books).filter(Books.Bid==Bid).first()
                    if(not Book):
                         raise NotFoundError(msg="Book  Not found")
                    BookName=Book.Name
                    BookReqDup=session.query(Requests).filter(Requests.Uid==userid,Requests.Bid==Bid).first()
                    if(BookReqDup):
                         raise ExistsError(msg="Request already sent!")
                    bookiss=session.query(books_issued).filter(books_issued.Bid==Bid,books_issued.Uid==userid).first()
                    if(bookiss):
                         raise ExistsError(msg="Books is already with you")
                    newReq=Requests(Uid=userid,UName=uname,Bid=Bid,BName=BookName,Status="pending")
                    session.add(newReq)
                    session.commit()
               cache.clear()
               return {"msg":"Request sent successfully"},200
          except NotFoundError as nfe:
               raise nfe
          except ExistsError as ee:
               raise ee
          except Exception as e:
               raise e
     @jwt_required()
     def put(self):
          try:
               user_id=get_jwt_identity()
               status=False
               with Session(engine) as session:
                    if(not user_id==0):
                         raise BussinessValidationError(msg="only admin can approve or reject request")
                    response=request.json.get('response')
                    if(response=='Accept'):
                         
                         current_date_time = datetime.now()
                         bid = request.json.get('Bid')
                         uid = request.json.get('Uid')
                         newBookIssued = books_issued(Uid=uid,Bid=bid,DateOfIssued=current_date_time.strftime('%Y-%m-%d'))
                         
                         req = session.query(Requests).filter(Requests.Bid==bid, Requests.Uid==uid).first()
                         req.Status = 'Accept'
                         status = True
                         session.delete(req)
                         session.add(newBookIssued)
                         session.commit()
                    else:
                         # add reject request
                         req=session.query(Requests).filter(Requests.Bid==request.json.get('Bid'),Requests.Uid==request.json.get('Uid')).first()
                         req.Status='Rejected'
                         session.delete(req)
                         session.commit()
               if(status):
                    cache.clear()
                    return {'msg':'Request accepted'},200
               else:
                    cache.clear()
                    return {'msg': 'Request Delined'},200
          except BussinessValidationError as bve:
               raise bve
api.add_resource(BookReq,"/api/BookReq")



class RequestsUsers(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self):
          userId=get_jwt_identity()
          with Session(engine) as session:
               reqs=session.query(Requests).filter(Requests.Uid==userId)
               temp=[]
               for i in reqs:
                    temp.append({'BName':i.BName,'Status':i.Status})
               return {'reqs':temp},200
api.add_resource(RequestsUsers,'/api/user/requests')


class BooksIssued(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self):
          uid=get_jwt_identity()
          if(uid!=0):
               print('uid:',uid)
               with Session(engine) as session:
                    mybooks=session.query(books_issued).filter(books_issued.Uid==uid).all()
                    temp=[]
                    for i in mybooks:
                         b=session.query(Books).filter(Books.Bid==i.Bid).first()
                         
                         temp.append(b.to_dict())
                    return {'Books':temp},200
          else:
               with Session(engine) as session:
                    mybooks=session.query(books_issued).all()
                    temp=[]
                    for i in mybooks:
                         b=session.query(Books).filter(Books.Bid==i.Bid).first()
                         temp.append({
                              'book':b.to_dict(),
                              'uid':i.Uid,
                              'date_of_issue':i.DateOfIssued
                         })
                    print(temp)
                    return temp,200
     @jwt_required()
     def delete(self):
          try:
               uid=get_jwt_identity()
               Bid=request.json.get('Bid')
               with Session(engine) as session:
                    if uid==0:
                         uid=request.json.get('Uid')
                    bi=session.query(books_issued).filter(books_issued.Uid==uid,books_issued.Bid==Bid).first()
                    if bi:
                         session.delete(bi)

                         session.commit()
                    else:
                         raise NotFoundError(msg='Book not found in issued')
               cache.clear()
               return {'msg':'Book Returned'},200
          except NotFoundError as nfe:
               raise nfe
          except Exception as e:
               raise e
api.add_resource(BooksIssued,"/api/booksIssued")


class RateBook(Resource):
     @jwt_required()
     def post(self):
          print("rating")
          uid=get_jwt_identity()
          bid=request.json.get('Bid')
          rate=int(request.json.get('Rating'))
          try:
               with Session(engine) as session:
                    book=session.query(Books).filter(Books.Bid==bid).first()
                    if(not book):
                         raise NotFoundError(msg="Book Not Found")
                    # (oldAvg*OldLen)+newRating/oldLen+1
                    oldLen=session.query(Ratings).filter(Ratings.Bid==bid).count()
                    oldAvg=book.AvgRating
                    if(oldAvg):
                         dupRating=session.query(Ratings).filter(Ratings.Uid==uid,Ratings.Bid==bid).first()
                         if(dupRating):
                              # newAvg=((oldAvg*len)-oldRating+newRating)/len
                              newAvgRating=((oldAvg*oldLen)-dupRating.Rating+rate)/oldLen
                              dupRating.Rating=rate
                         else:
                              newAvgRating=((oldAvg*float(oldLen))+rate)/(oldLen+1)
                              current_date = datetime.now()
                              formatted_date = current_date.strftime("%Y-%m-%d")  # Change format as needed
                              print("Formatted current date:", formatted_date)
                              newRating=Ratings(Uid=uid,Bid=bid,Rating=rate,CreatedDate=formatted_date)
                              session.add(newRating)
                    else:
                         newAvgRating=rate
                    
                    book.AvgRating=newAvgRating
                    session.commit()
               cache.clear()
               return {"msg":"success"},200
          except NotFoundError as nfe:
               raise nfe
          

api.add_resource(RateBook,"/api/Rating")

class ABook(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self,bid):
          try:
               uid=get_jwt_identity()
               if uid!=0:
                    return {"msg":"your not Librarian"},401
               with Session(engine) as session:
                    book = session.query(Books).filter(Books.Bid==bid).first()
                    if not book:
                         raise NotFoundError(msg="Book Not Found")
                    book=book.to_dict()
                    return book,200
          except NotFoundError as nfe:
               raise nfe
api.add_resource(ABook,"/api/getBook/<int:bid>")
# add  sections

class SectionsRes(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self):
          uid=get_jwt_identity()
          role='user'
          if uid==0:
               role='lib'
          with Session(engine) as session:
               sections=session.query(Sections).all()
               sectionsObj=[]
               for i in range(len(sections)):
                    secObj={
                    'Sid':sections[i].Sid,
                    'Sname':sections[i].SName
                    }
                    sectionsObj.append(secObj)
               res={
                    'role':role,
                    'secDetails':sectionsObj
               }
               return res,200
     @jwt_required()
     def post(self):
          uid=get_jwt_identity()
          if(uid!=0):
               return {"msg":"Your not admin"},401
          try:
               sname=request.json.get('sname')
               secbooks=request.json.get('Bids')
               with Session(engine) as session:
                    dupSec=session.query(Sections).filter(Sections.SName==sname).first()
                    if dupSec:
                         raise ExistsError(msg='Section Name already exists')
                    current_date = datetime.now()
                    formatted_date = current_date.strftime("%Y-%m-%d")  # Change format as needed
                    print("Formatted current date:", formatted_date)
                    newSec=Sections(SName=sname,CreatedDate=formatted_date)
                    session.add(newSec)
                    session.commit()
               with Session(engine) as session:
                    newSec=session.query(Sections).filter(Sections.SName==sname).first()
                    
                    for i in range(len(secbooks)):
                         newSecBook=sec_books(Sid=newSec.Sid,Bid=secbooks[i])
                         session.add(newSecBook)
                    session.commit()
               cache.clear()
               return {'msg':'Created Successfully'},200
          except ExistsError as ee:
               raise ee
     
     @jwt_required()
     def put(self):
          uid=get_jwt_identity()
          if(uid!=0):
               return {"msg":"Your not librarian"},401
          try:
               print()
               sid=request.json.get('sid')
               sname=request.json.get('sname')
               secbooksToAdd=request.json.get('selectedBids')
               print(secbooksToAdd)
               secbooksToRemove=request.json.get('unselectedBids')
               with Session(engine) as session:
                    section=session.query(Sections).filter(Sections.Sid==sid).first()
                    secDup=session.query(Sections).filter(Sections.SName==sname,Sections.Sid!=sid).first()
                    if secDup:
                         return {"msg":"Section name already in use"},409
                    section.SName=sname
                    sec_book=session.query(sec_books).filter(sec_books.Sid==sid).all()
                    #delete books from sec_book
                    for i in sec_book:
                         if(str(i.Bid) in secbooksToRemove):
                              session.delete(i)
                    # adding books
                    book=session.query(Books).all()
                    for i in book:
                         if str(i.Bid) in secbooksToAdd:
                              print(f"added :${i.Bid}")
                              newBookSec=sec_books(Sid=sid,Bid=i.Bid)
                              session.add(newBookSec)
                    session.commit()
               cache.clear()
               return {"msg":"modifed successfully"},200
          except NotFoundError as nfe:
               raise nfe
     
     @jwt_required()
     def delete(self):
          uid=get_jwt_identity()
          if(uid!=0):
               return {"msg":"Your not librarian"},401
          
          sid=request.json.get('sid')
          try:
               with Session(engine) as session:
                    secBooks=session.query(sec_books).filter(sec_books.Sid==sid).all()
                    if not secBooks:
                         raise NotFoundError(msg="books not found in section")
                    for i in secBooks:
                         session.delete(i)
                    sec=session.query(Sections).filter(Sections.Sid==sid).first()
                    session.delete(sec)
                    session.commit()
               cache.clear()
               return {'msg':'deleted succesfuly'}
          except NotFoundError as nfe:
               raise nfe
          
api.add_resource(SectionsRes,"/api/sections")

class Asection(Resource):
     @jwt_required()
     @cache.cached(timeout=50)
     def get(self,sid):

          try:
               role='user'
               uid=get_jwt_identity()
               if(uid==0):
                    role='lib'
               with Session(engine) as session:
                    sec=session.query(Sections).filter(Sections.Sid==sid).first()
                    if not sec:
                         raise NotFoundError
                    bookIds=session.query(sec_books).filter(sec_books.Sid==sid).all()
                    booksData=[]
                    for i in range(len(bookIds)):
                         book=session.query(Books).filter(Books.Bid==bookIds[i].Bid).first()
                         booksData.append(book.to_dict())
                    
                    res={
                         'userRole':role,
                         'SName':sec.SName,
                         'books':booksData
                    }
                    return res,200
          except NotFoundError as nfe:
               raise nfe
     def delete(self,sid):
          try:
               with Session(engine) as session:
                    Bid=request.json.get('Bid')
                    sec=session.query(Sections).filter(Sections.Sid==sid).first()
                    if not sec:
                         raise NotFoundError(msg="section not found")
                    secbook=session.query(sec_books).filter(sec_books.Sid==sid,sec_books.Bid==Bid).first()
                    if not secbook:
                         raise NotFoundError(msg='Book Not found in Section')
                    session.delete(secbook)
                    session.commit()
               cache.clear()
               return {'msg':'book is removed from section'}
          except NotFoundError as nfe:
               raise nfe
api.add_resource(Asection,'/api/getSection/<int:sid>')

class createSection(Resource):
     def get(self):
          try:
               eliBooks=[]
               with Session(engine) as session:
                    book=session.query(Books).all()

                    secBooks=session.query(sec_books).all()
                    for i in range(len(book)):
                         found=False
                         for j in range(len(secBooks)):
                              if(book[i].Bid==secBooks[j].Bid):
                                   found=True
                         if not found:
                              eliBooks.append(book[i].to_dict())
               if len(eliBooks)==0:
                    raise NotFoundError(msg="no books are present to add")
               return eliBooks,200
          except NotFoundError as nfe:
               raise nfe
api.add_resource(createSection,"/api/sectionCreate")

class ExportCSV(Resource):
     
     def get(self):
          task = csv_report()
          return {'msg':'csv file will be sent to your email please check'},200
api.add_resource(ExportCSV,'/api/export_csv')