"""Module containing report repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.report import ReportIn


class IReportRepository(ABC):
    """An abstract class representing protocol of report repository."""

    @abstractmethod
    async def get_report(self) -> Iterable[Any]:
        """The abstract getting report.

        Returns:
            Iterable[Report]: Report.
        """

    @abstractmethod
    async def get_report_by_city_name(self, city_name: str) -> Iterable[Any]:
        """The abstract getting report by city name.

        Returns:
            Iterable[Report]: Report.
        """

    @abstractmethod
    async def get_report_by_category_name(self, category_name: str) -> Iterable[Any]:
        """The abstract getting report by category name.

        Returns:
            Iterable[Report]: Report.
        """

