import time
from celery import Celery
from redis import Redis

from settings import Settings
from user_manager.core.draw import draw_helper
redis_conn = Redis()

settings = Settings()
# configure celery app with Redis as the message broker
app = Celery("draw_tasks",
             broker=f"{settings.celery_broker_url}/0",
             result_backend=f"{settings.celery_broker_url}/0")
DRAW_TASK_SET = "drawing_task_set"


def is_thread_in_set(thread_id):
    return redis_conn.sismember(DRAW_TASK_SET, thread_id)


def add_to_set(thread_id):
    redis_conn.sadd(DRAW_TASK_SET, thread_id)


def remove_from_set(thread_id):
    redis_conn.srem(DRAW_TASK_SET, thread_id)


@app.task(bind=True)
def draw(self, thread_id):
    try:
        # Perform the drawing task
        draw_helper(thread_id)
    finally:
        # Remove thread_id from the set after the task is completed
        remove_from_set(thread_id)

