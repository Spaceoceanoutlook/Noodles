from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from marshmallow import Schema, fields


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_of_country: Mapped[str] = mapped_column(String(30), unique=True)
    # Параметр перед relationship (Noodles) указывает на связанную модель,
    # а back_populates на атрибут этой модели (country)
    noodles: Mapped[list["Noodles"]] = relationship(back_populates="country", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Name={self.name_of_country}"

    def __str__(self):
        return f"Name={self.name_of_country}"


class Noodles(Base):
    __tablename__ = "noodles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_of_noodles: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None]
    recommendation: Mapped[bool]
    image: Mapped[str | None] = mapped_column(String(150))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    # Параметр в Mapped (Country) указывает на связанную модель,
    # а back_populates на атрибут Country, с которого мы попадаем сюда (noodles)
    country: Mapped["Country"] = relationship(back_populates="noodles")

    def __repr__(self):
        return f"Name={self.name_of_noodles}"

    def __str__(self):
        return f"Name={self.name_of_noodles}"


class NoodlesSchema(Schema):
    id = fields.Int(dump_only=True)
    name_of_noodles = fields.Str()
    description = fields.Str()
    recommendation = fields.Bool()
    image = fields.Str()
    country_id = fields.Int()


# Если без миграций, то можно создать таблицы, запустив этот модуль
# def create_table():
#     Base.metadata.create_all(bind=engine)
#
#
# if __name__ == '__main__':
#     create_table()
