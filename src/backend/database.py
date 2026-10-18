import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Image(Base):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    folder_id = Column(Integer, ForeignKey("Folder.id"), nullable=False)

    folder = relationship("Folder", back_populates="images")
    tags = relationship(
        "Tag",
        secondary="LinkImageTag",
        back_populates="images",
    )


class Folder(Base):
    __tablename__ = "Folder"

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)

    images = relationship("Image", back_populates="folder")


class Tag(Base):
    __tablename__ = "Tag"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    images = relationship(
        "Image",
        secondary="LinkImageTag",
        back_populates="tags",
    )


class LinkImageTag(Base):
    __tablename__ = "LinkImageTag"

    image_id = Column(
        Integer, ForeignKey("Image.id"), primary_key=True
    )
    tag_id = Column(
        Integer, ForeignKey("Tag.id"), primary_key=True
    )


def creat_db(path):

    engine = create_engine(f"sqlite:///{path}")

    Base.metadata.create_all(engine)

    return engine

def add_folder(path, engine):
    if id_folder(path, engine) == None:
        Session = sessionmaker(bind=engine)
        session = Session()

        folder = Folder(path=path)
        session.add(folder)
        session.commit()

        session.close()

def id_folder(path, engine):
    Session = sessionmaker(bind=engine)

    with Session() as session:
        folder_id = (
            session.query(Folder.id)
            .filter(Folder.path == path)
            .scalar()
        )

        return folder_id

def add_image(path, filename, engine):
    if id_image(filename, engine) == None:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            image = Image(filename=filename, folder_id = id_folder(path, engine))
            session.add(image)
            session.commit()

def id_image(filename, engine):
    Session = sessionmaker(bind=engine)

    with Session() as session:
        image_id = (
            session.query(Image.id)
            .filter(Image.filename == filename)
            .scalar()
        )

        return image_id

def add_tag(name, description, engine):
    if id_tag == None:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            tag = Tag(name=name, description=description)
            session.add(tag)
            session.commit()

def id_tag(name, engine):
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        tag_id = (
            session.query(Tag.id)
            .filter(Tag.name == name)
            .scalar()
        )
        return tag_id

# engine = creat_db(
#     r"C:\Users\mariu\Desktop\PY\Tagger\Test",
#     "bonjour",
# )

# add_folder("bite", engine)

# print(id_folder("bite", engine))