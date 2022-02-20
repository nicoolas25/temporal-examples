from __future__ import annotations

from dataclasses import dataclass, replace
from functools import reduce
from typing import List

from temporal.validity_period import ValidityPeriod

@dataclass(frozen=True)
class UnpaidLeave:
    validity_period: ValidityPeriod

@dataclass(frozen=True)
class DisabilityCoverage:
    validity_period: ValidityPeriod

    def slice(self, validity_period: ValidityPeriod) -> DisabilityCoverage:
        if not validity_period.is_included_in(self.validity_period):
            raise ValueError("Can't slice outside the original validity period")
        return replace(self, validity_period=validity_period)

def subtract_unpaid_leaves(
    disability_coverages: List[DisabilityCoverage],
    unpaid_leaves: List[UnpaidLeave],
) -> List[DisabilityCoverage]:
    """
    Subtract a list of UnpaidLeave from a list of DisabilityCoverage.

    This is useful as the disability coverage can exclude unpaid leave periods.
    """
    return reduce(
        _subtract_unpaid_leave_from_each_disability_coverage,
        unpaid_leaves,
        disability_coverages,
    )

def _subtract_unpaid_leave_from_each_disability_coverage(
    disability_coverages: List[DisabilityCoverage],
    unpaid_leave: UnpaidLeave,
) -> List[DisabilityCoverage]:
    """
    Subtract an unpaid leave from a list of DisabilityCoverage.

    Each DisabilityCoverage can be split into 0, 1, or 2 according to
    how they overlap with the UnpaidLeave.
    """
    return [
        disability_coverage.slice(validity_period)
        for disability_coverage in disability_coverages
        for validity_period in disability_coverage.validity_period.subtract(
            unpaid_leave.validity_period
        )
    ]
