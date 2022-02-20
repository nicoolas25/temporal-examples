from typing import Protocol

from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.expression import and_, or_

from temporal.validity_period import ValidityPeriod

class HasStartAndEndDateInstrumentedAttributes(Protocol):
    start_date: InstrumentedAttribute
    end_date: InstrumentedAttribute

class ValidityPeriodQueryHelper:
    def __init__(self, sqla_class: HasStartAndEndDateInstrumentedAttributes):
        self.start_date = sqla_class.start_date
        self.end_date = sqla_class.end_date

    def do_overlap(self, validity_period: ValidityPeriod):
        return and_(
            (
                validity_period.end_date is None
                or self.start_date <= validity_period.end_date
            ),
            or_(
                self.end_date >= validity_period.start_date,
                self.end_date == None,
            ),
        )
