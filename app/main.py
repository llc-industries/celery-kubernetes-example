"""
Simple Flask backend.
"""
import datetime
import logging
import os

import flask

import database
import settings
import tasks


flask_app = flask.Flask(__name__)
flask_app.logger.setLevel(logging.INFO)
_backend = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")
_broker = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq-service:5672")
flask_app.config.update(
        result_backend=_backend,
        broker_url=_broker,
        CELERY_RESULT_BACKEND=_backend,
        CELERY_BROKER_URL=_broker)

celery_app = tasks.make_celery(flask_app)


def timestamp2iso(t):
    return '' if t is None else datetime.datetime.fromtimestamp(t).isoformat()

@flask_app.route("/", methods=["GET"])
def get_index():
    return flask.render_template("index.html")

@flask_app.route("/tasks-json", methods=["GET"])
def get_tasks_json():
    all_tasks = []
    for task_id, created in database.get_all():
        async_res = celery_app.AsyncResult(task_id)
        is_ready = async_res.ready()
        res_str = ""
        finished_str = ""
        if is_ready:
            finished_str = "Completed"
            try:
                res_str = str(async_res.result) if async_res.successful() else "FAILED"
            except Exception:
                res_str = "ERROR"
        else:
            finished_str = async_res.state or "PENDING"
            
        all_tasks.append({
            "id": task_id,
            "created": timestamp2iso(created),
            "finished": finished_str,
            "result": res_str
        })
    return {"all_tasks": all_tasks}

@flask_app.route("/task", methods=["POST"])
def post_task():
    if not flask.request.is_json:
        flask_app.logger.warning("Invalid non-JSON request with content type '%s'", flask.request.content_type)
        flask.abort(405)
    data = flask.request.json
    str_a, str_b = data["str_a"], data["str_b"]
    task_id = tasks.create_lcs_task(str_a, str_b)
    flask_app.logger.info(
            "Created new task %s for computing LCS of str_a (%d chars) and str_b (%d chars)",
            task_id, len(str_a), len(str_b))
    return {"task_id": task_id}


if __name__ == "__main__":
    if not os.path.exists(settings.database_path):
        database.init()
        flask_app.logger.info("Created database %s", settings.database_path)
    else:
        flask_app.logger.info("Using existing database %s", settings.database_path)
    flask_app.run(host="0.0.0.0", port=5000)
