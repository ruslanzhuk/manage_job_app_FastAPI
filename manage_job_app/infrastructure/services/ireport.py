"""Module containing report service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from manage_job_app.core.domain.report import Report, ReportIn
from manage_job_app.infrastructure.dto.reportdto import ReportDTO


class IReportService(ABC):
    """A class representing report repository."""

    @abstractmethod
    async def get_report(self) -> Iterable[ReportDTO]:
        """The method getting reports from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """

    @abstractmethod
    async def get_report_by_city_name(self, city_name: str) -> Iterable[ReportDTO]:
        """The method getting reports by city name from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """

    @abstractmethod
    async def get_report_by_category_name(self, category_name: str) -> Iterable[ReportDTO]:
        """The method getting reports by category name from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """

