import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Shop, Publisher, Book, Stock, Sale

DSN = 'postgresql://postgres:16@localhost:5432/Book_guide'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
publisher1 = Publisher(name="Пушкин")
publisher2 = Publisher(name="Гоголь")
book1 = Book(title="Капитанская дочка", publisher=publisher1)
book2 = Book(title="Евгений Онегин", publisher=publisher1)
book3 = Book(title="Руслан и Людмила", publisher=publisher1)
book4 = Book(title="Мертвые души", publisher=publisher2)
shop1 = Shop(name="Буковед")
shop2 = Shop(name="Лабиринт")
shop3 = Shop(name="Книжный дом")
stock1 = Stock(book_stock=book1, shop_stock=shop1)
stock2 = Stock(book_stock=book3, shop_stock=shop1)
stock3 = Stock(book_stock=book1, shop_stock=shop2)
stock4 = Stock(book_stock=book2, shop_stock=shop3)
stock5 = Stock(book_stock=book1, shop_stock=shop1)
sale1 = Sale(price='600', date_sale='09-11-2022', stock=stock1, count=1)
sale2 = Sale(price='500', date_sale='08-11-2022', stock=stock2, count=1)
sale3 = Sale(price='580', date_sale= '05-11-2022', stock=stock3, count=1)
sale4 = Sale(price='490', date_sale = '02-11-2022', stock=stock4, count=1)
sale5 = Sale(price='600', date_sale = '26-10-2022', stock=stock5, count=1)

session.add_all([publisher1, publisher2, book1, book2, book3, book4,
                 shop1, shop2, shop3, stock1, stock2, stock3, stock4, stock5,
                 sale1, sale2, sale3, sale4, sale5])

name_publisher = input("Введите имя автора: ")
result = session.query(Publisher).join(Book).join(Stock).join(Shop).\
                   join(Sale).filter(Publisher.name == name_publisher)

for publ in result.all():
    for book in publ.books:
        for stock in book.stocks:
            for sale in stock.sales:
                print(f'{book.title} | {stock.shop_stock.name} |'
                      f' {sale.price} | {sale.date_sale}')

session.commit()
session.close()

--------------------------------MODELS-----------------------------------------------------
import psycopg2
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'
    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)
    def __str__(self):
        return f'{self.name}'


class Book(Base):
    __tablename__ = "books"
    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    title = sq.Column(sq.Text)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publishers.id"))
    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return f'{self.title} | {self.publisher}'


class Stock(Base):
    __tablename__ = 'stocks'
    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    id_books = sq.Column(sq.Integer, sq.ForeignKey('books.id'))
    id_shops = sq.Column(sq.Integer, sq.ForeignKey('shops.id'))

    book_stock = relationship("Book", backref="stocks")
    shop_stock = relationship("Shop", backref="stocks")


class Shop(Base):
    __tablename__ = 'shops'
    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)

    def __str__(self):
        return f'{self.name}'


class Sale(Base):
    __tablename__ = "sales"
    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stocks.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship("Stock", backref="sales")
    def __str__(self):
        return f'{self.price}, {self.date_sale}, {self.stock_id}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)