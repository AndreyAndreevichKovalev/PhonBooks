import os
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, join

from dotenv import load_dotenv


Base = declarative_base()

class Course(Base):
    __tablename__ = "course"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Homework(Base):
    __tablename__ = "homework"

    id = sq.Column(sq.Integer, primary_key=True)
    number = sq.Column(sq.Integer, nullable=False)
    description = sq.Column(sq.Text, nullable=False)
    course_id = sq.Column(sq.Integer, sq.ForeignKey("course.id"), nullable=False)

    course = relationship(Course, backref="homeworks")

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50))
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

load_dotenv()
DSN = os.getenv("DSN")
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# # создание объектов
# Pb1 = Publisher(name="O\u2019Reilly")
# Pb2 = Publisher(name="Pearson")
# Pb3 = Publisher(name="Microsoft Press")
# Pb4 = Publisher(name="No starch press")
#
# Bk1 = Book(title="Programming Python, 4th Edition", publisher_id=1)
# Bk2 = Book(title="Learning Python, 4th Edition", publisher_id=1)
# Bk3 = Book(title="Natural Language Processing with Python", publisher_id=1)
# Bk4 = Book(title="Hacking: The Art of Exploitation", publisher_id=4)
# Bk5 = Book(title="Modern Operating Systems", publisher_id=2)
# Bk6 = Book(title="Code Complete: Second Edition", publisher_id=3)
#
# Sh1 = Shop(name="Labirint")
# Sh2 = Shop(name="OZON")
# Sh3 = Shop(name="Amazon")
#
# St1 = Stock(id_shop=1, id_book=1, count=34)
# St2 = Stock(id_shop=1, id_book=2, count=30)
# St3 = Stock(id_shop=1, id_book=3, count=0)
# St4 = Stock(id_shop=2, id_book=5, count=40)
# St5 = Stock(id_shop=2, id_book=6, count=50)
# St6 = Stock(id_shop=3, id_book=4, count=10)
# St7 = Stock(id_shop=3, id_book=6, count=10)
# St8 = Stock(id_shop=2, id_book=1, count=10)
# St9 = Stock(id_shop=3, id_book=1, count=10)
#
# Sa1 = Sale(price="50.05", date_sale="2018-10-25T09:45:24.552Z)", id_stock=1, count=16)
# Sa2 = Sale(price="50.05", date_sale="2018-10-25T09:51:04.113Z)", id_stock=3, count=10)
# Sa3 = Sale(price="10.50", date_sale="2018-10-25T09:52:22.194Z)", id_stock=6, count=9)
# Sa4 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z)", id_stock=5, count=5)
# Sa5 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z)", id_stock=9, count=5)
# Sa6 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z)", id_stock=4, count=1)
#
# session.add_all([Pb1, Pb2, Pb3, Pb4,
#                  Bk1, Bk2, Bk3, Bk4, Bk5, Bk6,
#                  Sh1, Sh2, Sh3,
#                  St1, St2, St3, St4, St5, St6, St7, St8, St9,
#                  Sa1, Sa2, Sa3, Sa4, Sa5, Sa6])
# session.commit()
#
# # создание объектов
# js = Course(name="JavaScript")
# hw1 = Homework(number=1, description="первое задание", course=js)
# hw2 = Homework(number=3, description="второе задание (сложное)", course=js)
#
# session.add(js)
# session.add_all([hw1, hw2])
# session.commit()

# txt = input("Введите что-нибудь, чтобы проверить это: ")
# txt_num = int(txt)
# print("Это то, что вы только что ввели?", txt)

# publisher = Publisher()
# book = Book()

q = session.query(Publisher)\
    .join(Book.publisher)\
    .filter(Publisher.id == 1)\
    .all()

# for s in q:
#     print(s.id, s.name)
#     for p in s.book:
#         print("\t", p.id, p.title)
          #       for c in s.book

# запросы
# q = session.query(Course).join(Homework.course).filter(Course.id == 1)    # Homework.id
# # print(q)
# for s in q.all():
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)

# вложенный запрос
# subq = session.query(Homework).filter(Homework.description.like("%сложн%")).subquery("simple_hw")
# q = session.query(Course).join(subq, Course.id == subq.c.course_id)
# # print(q)
# for s in q.all():
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)

# обновление объектов
# session.query(Course).filter(Course.name == "JavaScript").update({"name": "NEW JavaScript"})
# session.commit()

# # удаление объектов
# session.query(Homework).filter(Homework.number > 1).delete()
# session.commit()  # фиксируем изменения