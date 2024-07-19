from fastapi import APIRouter
from user_manager.core.chat import submit_edited_image
from user_manager.core.file import get_latest_file
from user_manager.core.open_ai import get_image_description, make_image_edit
from user_manager.celery.tasks import add_to_set, draw as draw_task, is_thread_in_set
router = APIRouter()

PROMPT = "Complete this image based on what the user is trying to make: ({}), only add 5% more to the end goal of the image"


@router.get("/")
async def get():
    return "hello"


@router.post("/draw/{thread_id}")
async def draw(thread_id):
    if not is_thread_in_set(thread_id):
        # Add thread_id to the set before queuing the task
        add_to_set(thread_id)
        draw_task.delay(thread_id)
    else:
        print(f"Dropping the task: {thread_id}")
    return {"message": f"Successfully edited_image"}


