from sqlalchemy import *
import bcrypt
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
base = declarative_base(metadata=metadata)


def make_pwd_hash(pwd: str) -> str:
    return (bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())).decode()


def check_pwd(pwd: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(pwd.encode(), pwd_hash.encode())


users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('email', String(120)),
    Column('password_hash', String(128), nullable=False)
)


class A(base):
    __tablename__ = 'a'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(255), nullable=False, default='')


print(metadata.tables)
tb_a = metadata.tables["a"]
if __name__ == '__main__':
    a = make_pwd_hash('admin123456')
    print(a)
    print(check_pwd('admin123456', a))
