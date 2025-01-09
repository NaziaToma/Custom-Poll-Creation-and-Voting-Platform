from django.apps import AppConfig

class PollsConfig(AppConfig):
    name = 'polls'

    def ready(self):
        import polls.templatetags.bootstrap_filters
