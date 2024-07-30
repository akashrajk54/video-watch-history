from django.apps import AppConfig


class ElasticsearchConfig(AppConfig):
    name = 'elasticsearchs'

    def ready(self):
        import elasticsearchs.signals  # Ensure this matches your app's name and path
