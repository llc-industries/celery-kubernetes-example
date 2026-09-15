FROM myproject:1

WORKDIR /usr/src/myproject

ENTRYPOINT ["celery", "-A", "main.celery_app", "worker"]
