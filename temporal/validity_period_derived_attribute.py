from temporal.validity_period import ValidityPeriod
from temporal.validity_period_query_helper import HasStartAndEndDateInstrumentedAttributes, ValidityPeriodQueryHelper

class ValidityPeriodDerivedAttribute:
    def __get__(self, obj, objtype=None):
        if obj is not None:
            # Read the value
            return ValidityPeriod(
                start_date=getattr(obj, "start_date"),
                end_date=getattr(obj, "end_date"),
            )
        elif isinstance(objtype, HasStartAndEndDateInstrumentedAttributes):
            # Build a query builder for SQL Alchemy
            return ValidityPeriodQueryHelper(sqla_class=objtype)
        else:
            raise ValueError(f"Type '{objtype}' can't access a ValidityPeriodDerivedAttribute")

    def __set__(self, obj, value: ValidityPeriod):
        if obj is not None:
            setattr(obj, "start_date", value.start_date)
            setattr(obj, "end_date", value.end_date)
        else:
            raise ValueError("Can only set a ValidityPeriodDerivedAttribute on an instance")
