"""Module containing report service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5

from manage_job_app.core.domain.report import Report, ReportIn
from manage_job_app.core.repositories.ireport import IReportRepository
from manage_job_app.infrastructure.dto.reportdto import ReportDTO
from manage_job_app.infrastructure.services.ireport import IReportService


class ReportService(IReportService):
    """A class representing report repository."""

    _repository: IReportRepository

    def __init__(self, repository: IReportRepository) -> None:
        """The initializer of the `report service`.

        Args:
            repository (IReportRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_report(self) -> Iterable[ReportDTO]:
        """The method getting report from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """

        return await self._repository.get_report()

    async def get_report_by_city_name(self, city_name: str) -> Iterable[ReportDTO]:
        """The method getting report by city name from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """

        return await self._repository.get_report_by_city_name(city_name)


    async def get_report_by_category_name(self, category_name: str) -> Iterable[ReportDTO]:
        """The method getting report by category name from the repository.

        Returns:
            Iterable[ReportDTO]: report.
        """

        return await self._repository.get_report_by_category_name(category_name)