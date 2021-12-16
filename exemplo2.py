import strawberry
from typing import Optional
from sqlalchemy.sql.expression import table
from sqlmodel import (
    SQLModel,
    Field,
    create_engine,
    select,
    Session

)
from strawberry.custom_scalar import identity

engine = create_engine('sqlite:///database.db')

class Person(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: str

SQLModel.metadata.create_all(engine)

def create_object(nome: str, idade: int):
    person = Person(nome=nome, idade=idade)
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
    return person


@strawberry.type
class Pessoa:
    id: Optional[int]
    nome: str
    idade: int

@strawberry.type    
class Query:

    @strawberry.field
    def all_pessoas(self) -> list[Pessoa]:
        query = select(Person)
        with Session(engine) as session:
            result = session.execute(query).scalars().all()
        return result

@strawberry.type
class Mutation:

    create_person: Pessoa = strawberry.field(resolver=create_object)

schema = strawberry.Schema(query=Query, mutation=Mutation)
