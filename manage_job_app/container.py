"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from manage_job_app.infrastructure.repositories.offerdb import \
    OfferRepository
from manage_job_app.infrastructure.repositories.userdb import \
    UserRepository
from manage_job_app.infrastructure.repositories.applicationdb import \
    ApplicationRepository
from manage_job_app.infrastructure.repositories.reviewdb import \
    ReviewRepository
from manage_job_app.infrastructure.repositories.reportdb import \
    ReportRepository
from manage_job_app.infrastructure.repositories.continentdb import \
    ContinentRepository
from manage_job_app.infrastructure.repositories.countrydb import \
    CountryRepository
from manage_job_app.infrastructure.repositories.citydb import \
    CityRepository
from manage_job_app.infrastructure.repositories.job_categorydb import \
    CategoryRepository
from manage_job_app.infrastructure.repositories.admindb import \
    AdminRepository

from manage_job_app.infrastructure.services.offer import OfferService
from manage_job_app.infrastructure.services.user import UserService
from manage_job_app.infrastructure.services.application import ApplicationService
from manage_job_app.infrastructure.services.review import ReviewService
from manage_job_app.infrastructure.services.report import ReportService
from manage_job_app.infrastructure.services.continent import ContinentService
from manage_job_app.infrastructure.services.country import CountryService
from manage_job_app.infrastructure.services.city import CityService
from manage_job_app.infrastructure.services.job_category import CategoryService
from manage_job_app.infrastructure.services.admin import AdminService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    offer_repository = Singleton(OfferRepository)
    user_repository = Singleton(UserRepository)
    application_repository = Singleton(ApplicationRepository)
    review_repository = Singleton(ReviewRepository)
    report_repository = Singleton(ReportRepository)
    continent_repository = Singleton(ContinentRepository)
    country_repository = Singleton(CountryRepository)
    city_repository = Singleton(CityRepository)
    category_repository = Singleton(CategoryRepository)
    admin_repository = Singleton(AdminRepository)


    offer_service = Factory(
        OfferService,
        repository=offer_repository,
    )
    user_service = Factory(
        UserService,
        repository=user_repository,
    )
    application_service = Factory(
        ApplicationService,
        repository=application_repository,
    )
    review_service = Factory(
        ReviewService,
        repository=review_repository,
    )
    report_service = Factory(
        ReportService,
        repository=report_repository,
    )
    continent_service = Factory(
        ContinentService,
        repository=continent_repository,
    )
    country_service = Factory(
        CountryService,
        repository=country_repository,
    )
    city_service = Factory(
        CityService,
        repository=city_repository,
    )
    category_service = Factory(
        CategoryService,
        repository=category_repository,
    )
    admin_service = Factory(
        AdminService,
        repository=admin_repository,
    )

