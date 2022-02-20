from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional

@dataclass(frozen=True)
class ValidityPeriod:
    start_date: date
    end_date: Optional[date]

    def is_active(self, on_date) -> bool:
        return self._end_date >= on_date and self.start_date <= on_date

    def is_included_in(self, other: ValidityPeriod) -> bool:
        return (
            other.start_date <= self.start_date
            and other._end_date >= self._end_date
        )

    def do_overlap(self, other: ValidityPeriod) -> bool:
        return (
            self.start_date <= other._end_date
            and self._end_date >= other.start_date
        )

    def subtract(self, other: ValidityPeriod) -> List[ValidityPeriod]:
        if self.is_included_in(other):
            return []
        elif not self.do_overlap(other):
            return [self]
        elif self._end_date <= other._end_date or other.end_date is None:
            return [
                ValidityPeriod(
                    start_date=self.start_date,
                    end_date=other.start_date - timedelta(days=1),
                )
            ]
        elif self.start_date >= other.start_date:
            return [
                ValidityPeriod(
                    start_date=other.end_date + timedelta(days=1),
                    end_date=self.end_date,
                )
            ]
        else:
            return [
                ValidityPeriod(
                    start_date=self.start_date,
                    end_date=other.start_date - timedelta(days=1),
                ),
                ValidityPeriod(
                    start_date=other.end_date + timedelta(days=1),
                    end_date=self.end_date,
                )
            ]

    @property
    def _end_date(self) -> date:
        """Approximation to avoid `end_date is None` checks."""
        return self.end_date or date.max

    def __post_init__(self):
        if self.start_date > self._end_date:
            raise ValueError(
                "Invalid ValidityPeriod: start_date is after end_date"
            )
