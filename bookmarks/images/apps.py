from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self) -> None:
        # import signal handlers
        import images.signals
        return super().ready()