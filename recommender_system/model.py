from sqlalchemy import Table, Column, Integer, String, MetaData, UniqueConstraint, create_engine, ForeignKey, BIGINT, Text, DATETIME
from base import session, Base, engine
import pandas as pd


class Review(Base):
    __tablename__ = 'review'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', Integer, nullable=False)
    user_id = Column('user_id', BIGINT, nullable=False)
    username = Column('username', String(127), nullable=False)
    rating = Column('rating', Integer, nullable=False)
    comment = Column('comment', Text, nullable=False)
    time = Column('time', DATETIME, nullable=False)
    order_id = Column('order_id', BIGINT, nullable=False)

    def __init__(self, id, product_id, user_id, username, rating, comment, time, order_id):
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.username = username
        self.rating = rating
        self.comment = comment
        self.time = time
        self.order_id = order_id


def get_reviews():
    data = []
    try:
        reviews = session.query(Review).all()
        session.commit()
        for review in reviews:
            temp = {'user_id': review.user_id, 'item_id': review.product_id, 'rating': review.rating}
            data.append(temp)
        return data
    except Exception as e:
        session.rollback()
        print(e)
        return None


def dataframe_to_sql(name, dataframe):
    df = pd.DataFrame(dataframe)
    db = engine.connect()
    try:
        df.to_sql(name, db)
    except ValueError as e:
        print(e)
    else:
        print("Table %s created successfully." % name)
    finally:
        db.close()



if __name__ == '__main__':
    Base.metadata.create_all(engine)