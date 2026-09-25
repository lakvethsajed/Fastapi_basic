
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text

class Post(Base):
    __tablename__ = "addbooks"

    id = Column(Integer, primary_key = True, autoincrement=True)
    title = Column(String, nullable = False)
    author = Column(String, nullable = False)
    genre = Column(String, nullable = False)
    available = Column(Boolean, server_default = 'TRUE')
    description = Column(String)
    total_copies = Column(Integer, nullable = False, server_default = '1')
    available_copies = Column(Integer, nullable = False, server_default = '1')
    created_at = Column(TIMESTAMP , nullable = False, server_default= text('now()') )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String, nullable = False)
    username = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    role = Column(String, nullable = False, server_default = "user")
    created_at = Column(TIMESTAMP , nullable = False, server_default= text('now()') )
class Bookissue(Base):
    __tablename__ = "issuebooks"

    id = Column(Integer , primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("addbooks.id", ondelete = "CASCADE"), nullable = False)
    issued_at = Column(TIMESTAMP, nullable = False, server_default = text('now()'))
    due_date = Column(TIMESTAMP , nullable = False)
    returned_at = Column(TIMESTAMP)

class Login_session(Base):
    __tablename__ = "Token_store"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
    Token = Column(String, nullable = False)
    created_at = Column(TIMESTAMP,nullable=False, server_default= text('now()'))
    expiry_time = Column(TIMESTAMP, nullable=False)
    revoked = Column(Boolean, nullable=False, server_default='False')