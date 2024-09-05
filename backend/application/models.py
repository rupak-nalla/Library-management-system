from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable
db = SQLAlchemy()

class Users(db.Model):
     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     Name = db.Column(db.String(80), nullable=False)
     BCount = db.Column(db.Integer, nullable=False, default=0)
     Password = db.Column(db.String(80), nullable=False)  
     ProfileImg = db.Column(db.String(200))  
     Email = db.Column(db.String(120), nullable=False)  
     LoginTime=db.Column(db.String(120))


class Books(db.Model):
     Bid = db.Column(db.Integer, primary_key=True, autoincrement=True)
     Name = db.Column(db.String(200), nullable=False)  
     AuthorName = db.Column(db.String(200), nullable=False)  
     CoverPath=db.Column(db.String(200))
     AvgRating = db.Column(db.Float)
     CreatedDate=db.Column(db.String(200))
     Content=db.Column(db.String(200))
     def to_dict(self):
          return {
               'Bid': self.Bid,
               'Name': self.Name,
               'AuthorName': self.AuthorName,
               'AvgRating': self.AvgRating,
               'CoverPath':self.CoverPath,
               'CreatedDate':self.CreatedDate,
               'Content':self.Content
          }

class Sections(db.Model):
     Sid = db.Column(db.Integer, autoincrement=True, primary_key=True)
     SName = db.Column(db.String(200))  
     CreatedDate=db.Column(db.String(200))

class Requests(db.Model):
     Bid = db.Column(db.Integer, db.ForeignKey("books.Bid"), primary_key=True)
     Uid = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
     BName = db.Column(db.String(200))  
     UName = db.Column(db.String(200))  
     Status = db.Column(db.String(200))  

class books_issued(db.Model):
     Bid = db.Column(db.Integer, db.ForeignKey("books.Bid"), primary_key=True)
     Uid = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
     DateOfIssued = db.Column(db.String)

class Ratings(db.Model):
     Uid = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
     Bid = db.Column(db.Integer, db.ForeignKey("books.Bid"), primary_key=True)
     Rating = db.Column(db.Integer)
     CreatedDate=db.Column(db.String(200))

class sec_books(db.Model):
     Bid = db.Column(db.Integer, db.ForeignKey("books.Bid"), primary_key=True)
     Sid = db.Column(db.Integer, db.ForeignKey("sections.Sid"), primary_key=True)
