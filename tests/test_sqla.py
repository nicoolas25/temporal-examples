from datetime import date

from pytest import fixture
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Date, create_engine

from temporal.validity_period import ValidityPeriod
from temporal.validity_period_derived_attribute import ValidityPeriodDerivedAttribute

# Setup a test model
Base = declarative_base()
class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    validity_period = ValidityPeriodDerivedAttribute()

# Setup a test database, in memory
engine = create_engine('sqlite://')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def test_attributes():
    model = Model(start_date=date(2022, 1, 1))
    assert model.validity_period.is_active(date(2022, 6, 15))
    assert not model.validity_period.is_active(date(2021, 12, 31))

def test_queries(db_session):
    validity_period = ValidityPeriod(date(2022, 1, 1), date(2022, 1, 31))
    query = db_session.query(Model).filter(Model.validity_period.do_overlap(validity_period))
    assert str(query) == (
        "SELECT models.id AS models_id, models.start_date AS models_start_date, models.end_date AS models_end_date \n"
        "FROM models \n"
        "WHERE models.start_date <= ? AND (models.end_date >= ? OR models.end_date IS NULL)"
    )

    validity_period = ValidityPeriod(date(2022, 1, 1), None)
    query = db_session.query(Model).filter(Model.validity_period.do_overlap(validity_period))
    assert str(query) == (
        "SELECT models.id AS models_id, models.start_date AS models_start_date, models.end_date AS models_end_date \n"
        "FROM models \n"
        "WHERE models.end_date >= ? OR models.end_date IS NULL"
    )

@fixture
def db_session():
    connection = engine.connect()
    connection.execute(Model.__table__.delete())
    return Session()
