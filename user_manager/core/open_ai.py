from fastapi import WebSocket
from openai import OpenAI
from typing import BinaryIO
import time
from user_manager.core.db_api import get_prompt
from settings import Settings
import base64
from PIL import Image

client = OpenAI()

settings = Settings()

# MODEL_NAME = "gpt-3.5-turbo"
MODEL_NAME = "gpt-4-turbo"


def make_image_transparent(image_path: str):
    img = Image.open(f"images/{image_path}.png")
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    img.save(f"images/{image_path}_masked.png", "PNG")


def make_image_edit(image_path: str, prompt: str):
    make_image_transparent(image_path)
    image_objects = client.images.edit(
        image=open(f"images/{image_path}.png", "rb"),
        mask=open(f"images/{image_path}_masked.png", "rb"),
        prompt=prompt,
        size="1024x1024",
        response_format="b64_json"
    )
    image_data = image_objects.data[0].b64_json
    with open(f"images/{image_path}_edited.png", 'wb') as f:
        f.write(base64.b64decode(image_data))
    return image_objects


def get_image_description(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    run = client.beta.threads.runs.create(
        assistant_id=settings.assistant_id,
        thread_id=thread_id
    )
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=run.thread_id,
            run_id=run.id
        )
    thread_messages = client.beta.threads.messages.list(
        thread_id=run.thread_id,
        run_id=run.id
    )
    for msg in thread_messages.data:
        client.beta.threads.messages.delete(
            message_id=msg.id,
            thread_id=run.thread_id,
        )
    return thread_messages.data[0].content[0].text.value
