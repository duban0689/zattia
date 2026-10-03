"""Interface for fetching product data from an authorized external source.

No scraping and no unauthorized data collection from Amazon is performed
anywhere in this project. Today, `MockAmazonProductService` is the only
implementation, and it only returns clearly-labeled demo data defined in
code. When this project is connected to an authorized source (e.g. the
Amazon Product Advertising API, once the account qualifies for it), add a
new implementation of `AmazonProductService` here and swap it in wherever
`MockAmazonProductService` is currently used — the rest of the app (models,
views, templates) does not need to change.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExternalProductData:
    asin: str
    name: str
    description: str = ""
    price: float | None = None
    currency: str = "USD"
    rating: float | None = None
    review_count: int = 0
    image_url: str = ""
    features: list[str] = field(default_factory=list)


class AmazonProductService(ABC):
    """Authorized data source contract. Implementations must only use
    officially sanctioned APIs/feeds — never scraping."""

    @abstractmethod
    def get_product(self, asin: str) -> ExternalProductData | None:
        raise NotImplementedError

    @abstractmethod
    def search_products(self, query: str) -> list[ExternalProductData]:
        raise NotImplementedError


class MockAmazonProductService(AmazonProductService):
    """Development/demo stand-in. Returns clearly-fake data, never calls
    any network service. Used by `seed_demo` to populate the catalog before
    a real, authorized product data source is connected."""

    _demo_catalog = [
        ExternalProductData(
            asin="B0DEMO0001",
            name="Audífonos inalámbricos Demo X1",
            description="Audífonos de ejemplo con cancelación de ruido — dato de demostración, no es información real de Amazon.",
            price=59.99,
            rating=4.5,
            review_count=1280,
            features=[
                "Cancelación de ruido activa",
                "20 horas de batería",
                "Resistentes al agua IPX4",
            ],
        ),
    ]

    def get_product(self, asin: str) -> ExternalProductData | None:
        for item in self._demo_catalog:
            if item.asin == asin:
                return item
        return None

    def search_products(self, query: str) -> list[ExternalProductData]:
        q = query.lower()
        return [item for item in self._demo_catalog if q in item.name.lower()]
