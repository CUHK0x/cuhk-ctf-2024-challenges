from sqlalchemy import Column, Integer, String

from database import Base


class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    type1 = Column(String)
    type2 = Column(String, index=True)
    abilities = Column(String)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    spattack = Column(Integer)
    spdefense = Column(Integer)
    speed = Column(Integer)

    def __str__(self):
        return str(self.__dict__)

class Digimon(Base):
    __tablename__ = "digimons"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    level = Column(String)
    type = Column(String)
    attribute = Column(String)
    description = Column(String)
    flag = Column(String)
    tokenf0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b = Column(String)
    tokend743cb4b22397cf64e0117fd83d29ca1e059c698b8155a3771417e24458e2bb5 = Column(String)
    tokenb20e3fc8e392aeae90db75a40648ad4aa87d13830ef9eb80343b960130ec2d3e = Column(String) # This is the flag column, flagishereIguessright

    def __str__(self):
        return str(self.__dict__)
