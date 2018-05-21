from celery import Celery


class FlaskCelery(Celery):
    """
    Base Celery object.
    """
    def __init__(self, app=None, config=None):
        if not (config is None or isinstance(config, dict)):
            raise ValueError('`config` must be an instance of dict or None.')

        self.config = config

        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        """
        Initialize obj with the flask app context.
        """
        if not (config is None or isinstance(config, dict)):
            raise ValueError('`config` must be an instance of dict or None.')

        super().__init__(
            app.import_name,
            broker=app.config['CELERY_BROKER_URL'],
            backend=app.config['CELERY_RESULT_BACKEND']
        )
        self.conf.update(app.config)

        TaskBase = self.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask
        return self
