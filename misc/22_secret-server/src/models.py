from sqlalchemy import Column, Integer, String, BigInteger

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    platformName = Column(String)
    discordId = Column(BigInteger)
    discordTag = Column(String)

    def __str__(self):
        return str(self.__dict__)
