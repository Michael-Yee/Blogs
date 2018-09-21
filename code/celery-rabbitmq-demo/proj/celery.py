from celery import Celery


app = Celery('proj')
app.config_from_object('proj.celeryconfig')


if __name__ == '__main__':
    app.start()
