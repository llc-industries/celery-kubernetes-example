"""
Interface for launching asynchronous Celery tasks.
"""
import celery
import lcs.tasks

import database
import settings


def make_celery(app):
    # https://flask.palletsprojects.com/en/1.1.x/patterns/celery/
    backend = app.config.get('result_backend') or app.config.get('CELERY_RESULT_BACKEND')
    broker = app.config.get('broker_url') or app.config.get('CELERY_BROKER_URL')
    c = celery.Celery(
        app.import_name,
        backend=backend,
        broker=broker
    )
    c.conf.update(app.config)
    class ContextTask(c.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    c.Task = ContextTask
    return c

def create_lcs_task(str_a, str_b):
    """
    Create new async task to compute lcs on str_a and str_b.
    Sends directly to the single 'tasks' queue.
    """
    async_result = lcs.tasks.longest_common_substr.apply_async(
        (str_a, str_b),
        queue="tasks"
    )
    database.create_task(async_result.id)
    return async_result.id
