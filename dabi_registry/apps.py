from abstract.apps import AbstractConfig
from .loader import DabiRegistryLoader
from .elastic_models import ElasticDabiRegistryModel, dabi_registry_idx


class DabiRegistryConfig(AbstractConfig):
    name = "dabi_registry"

    verbose_name = "Реєстр дозволів ДАБІ"
    short_name = "ДАБІ"
    loader_class = DabiRegistryLoader

    @property
    def data_model(self):
        # Doing that to prevent circular imports of some kind
        from .models import DabiRegistryModel

        return DabiRegistryModel

    @property
    def sitemap(self):
        from .sitemaps import DabiRegistrySitemap

        return DabiRegistrySitemap

    elastic_model = ElasticDabiRegistryModel
    elastic_index = dabi_registry_idx
