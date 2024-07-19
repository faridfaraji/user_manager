from user_manager.core.chat import submit_edited_image
from user_manager.core.file import get_latest_file
from user_manager.core.open_ai import get_image_description, make_image_edit

PROMPT = "Complete this image based on what the user is trying to make: ({}), only add 5% more to the end goal of the image"


def draw_helper(thread_id):
    filename = f"images/{str(thread_id)}.png"
    get_latest_file(thread_id, filename)
    print("Getting the latest file")
    image_description = get_image_description(thread_id)
    print("Getting the image description")
    prompt = PROMPT.format(image_description)
    make_image_edit(thread_id, prompt)
    print("making the image edit")
    submit_edited_image(thread_id, f"images/{thread_id}_edited.png")
    print("Submitting the image edit")
    return {"message": f"Successfully edited_image"}
