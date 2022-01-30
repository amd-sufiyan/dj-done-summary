from django.apps import AppConfig


class FrontPageConfig(AppConfig):
		name = 'frontpage'

		def ready(self):
			from jobs import update
			update.start()
			print('ready')
