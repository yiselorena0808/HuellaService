from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base


class User(Base):
    __tablename__ = 'huellas'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer)
    huella_template = Column(LargeBinary)

