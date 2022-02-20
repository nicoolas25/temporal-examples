from datetime import date

from temporal.composition_example import DisabilityCoverage, UnpaidLeave, subtract_unpaid_leaves
from temporal.validity_period import ValidityPeriod

def test_subtract_unpaid_leaves():
    # Unpaid leave covers all disability coverage
    assert _subtract_unpaid_leaves(
        [(date(2022, 1, 1), date(2022, 12, 31))],
        [(date(2021, 1, 1), date(2022, 12, 31))],
    ) == []

    # No overlap
    assert _subtract_unpaid_leaves(
        [(date(2022, 1, 1), None)],
        [(date(2021, 1, 1), date(2021, 12, 31))],
    ) == [DisabilityCoverage(ValidityPeriod(date(2022, 1, 1), None))]

    # Overlap at the begining
    assert _subtract_unpaid_leaves(
        [(date(2022, 1, 1), None)],
        [(date(2021, 1, 1), date(2022, 3, 31))],
    ) == [DisabilityCoverage(ValidityPeriod(date(2022, 4, 1), None))]

    # Overlap at the end
    assert _subtract_unpaid_leaves(
        [(date(2022, 1, 1), date(2022, 12, 31))],
        [(date(2022, 6, 1), None)],
    ) == [DisabilityCoverage(ValidityPeriod(date(2022, 1, 1), date(2022, 5, 31)))]

    # Overlap in the middle
    assert _subtract_unpaid_leaves(
        [(date(2022, 1, 1), date(2022, 12, 31))],
        [(date(2022, 6, 1), date(2022, 9, 1))],
    ) == [
        DisabilityCoverage(ValidityPeriod(date(2022, 1, 1), date(2022, 5, 31))),
        DisabilityCoverage(ValidityPeriod(date(2022, 9, 2), date(2022, 12, 31))),
    ]

    # Multiple overlaps
    assert _subtract_unpaid_leaves(
        [
            (date(2022, 1, 1), date(2022, 12, 31)),
            (date(2023, 1, 1), date(2023, 12, 31)),
        ],
        [
            (date(2022, 6, 1), date(2022, 9, 1)),
            (date(2022, 12, 1), date(2023, 9, 1)),
        ],
    ) == [
        DisabilityCoverage(ValidityPeriod(date(2022, 1, 1), date(2022, 5, 31))),
        DisabilityCoverage(ValidityPeriod(date(2022, 9, 2), date(2022, 11, 30))),
        DisabilityCoverage(ValidityPeriod(date(2023, 9, 2), date(2023, 12, 31))),
    ]


def _subtract_unpaid_leaves(disability_coverages, unpaid_leaves):
    return subtract_unpaid_leaves(
        disability_coverages=[
            DisabilityCoverage(validity_period=ValidityPeriod(start_date, end_date))
            for start_date, end_date in disability_coverages
        ],
        unpaid_leaves=[
            UnpaidLeave(validity_period=ValidityPeriod(start_date, end_date))
            for start_date, end_date in unpaid_leaves
        ]
    )
