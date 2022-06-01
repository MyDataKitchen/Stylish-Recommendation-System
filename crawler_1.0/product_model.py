from sqlalchemy import Table, Column, Integer, String, MetaData, UniqueConstraint, create_engine, ForeignKey, BIGINT, Text
from base import session, Base, engine

Base.metadata.create_all(engine)

class Product(Base):
    __tablename__ = 'product'
    id = Column('id', BIGINT, primary_key=True)
    category = Column('category', String(127), nullable=False)
    title = Column('title', String(255), nullable=False)
    description = Column('description', String(255), nullable=False)
    price = Column('price', Integer, nullable=False)
    texture = Column('texture', String(127), nullable=False)
    wash = Column('wash', String(127), nullable=False)
    place = Column('place', String(127), nullable=False)
    note = Column('note', String(127), nullable=False)
    story = Column('story', Text, nullable=False)
    main_image = Column('main_image', String(255), nullable=False)


    def __init__(self, id, category, title, description, price, texture, wash, place, note, story, main_image):
        self.id = id
        self.category = category
        self.title = title
        self.description = description
        self.price = price
        self.texture = texture
        self.wash = wash
        self.place = place
        self.note = note
        self.story = story
        self.main_image = main_image


class Variant(Base):
    __tablename__ = 'variant'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', BIGINT, ForeignKey('product.id'), nullable=False)
    color_id = Column('color_id', Integer, nullable=False)
    size = Column('size', String(15), nullable=False)
    stock = Column('stock', Integer, nullable=False)

    def __init__(self, product_id, color_id, size, stock):
        self.product_id = product_id
        self.color_id = color_id
        self.size = size
        self.stock = stock


class ProductImages(Base):
    __tablename__ = 'product_images'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', BIGINT, ForeignKey('product.id'), nullable=False)
    image = Column('image', String(100))

    def __init__(self, product_id, image):
        self.product_id = product_id
        self.image = image


def insert_product(product):
    try:
        new_product = Product(**product)
        session.add(new_product)
        session.commit()
        return new_product.id
    except Exception as e:
        session.rollback()
        print(e)
        return None


def insert_variant(variant):
    try:
        new_variant = Variant(**variant)
        session.add(new_variant)
        session.commit()
        return new_variant.id
    except Exception as e:
        session.rollback()
        print(e)
        return None


def insert_image(image):
    try:
        new_image = ProductImages(**image)
        session.add(new_image)
        session.commit()
        return new_image.id
    except Exception as e:
        session.rollback()
        print(e)
        return None

if __name__ == '__main__':
    Base.metadata.create_all(engine)