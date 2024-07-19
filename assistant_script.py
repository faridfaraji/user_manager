from openai import OpenAI
import json
import time

client = OpenAI()


def load_assistant():
    with open("art_assistant.json", "r") as file:
        data = json.load(file)
    return data


def store_assistant(assistant):
    with open("art_assistant.json", "w") as file:
        # Write a string to the file
        file.write(json.dumps(assistant))


def create_assistant(name, model, instruction):
    id = client.beta.assistants.create(
        instructions=instruction,
        name=name,
        model=model
    ).id
    print(id)
    return id


def update_assistant(assistant, model, instruction):
    return client.beta.assistants.update(
        assistant.get("id"),
        instructions=instruction,
        name=assistant.name,
        model=model
    )


def to_dict(assistant):
    return {
        "id": assistant.id,
        "object": assistant.object,
        "created_at": assistant.created_at,
        "name": assistant.name,
        "description": assistant.description,
        "instructions": assistant.instructions
    }


def run_assistant_on_thread(assistant_id, thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    while run.status not in ["cancelled", "failed", "completed"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        time.sleep(0.2)
    thread_messages = client.beta.threads.messages.list(thread_id)
    print(thread_messages.data[0].content[0].text.value)


def delete_art_asistant_messages(assistant_id, thread_id):
    messages = client.beta.threads.messages.list(thread_id)
    for message in messages:
        if message.assistant_id == assistant_id:
            print(f"deleting message {message.id}")
            client.beta.threads.messages.delete(
                message_id=message.id,
                thread_id=thread_id,
            )

ARTIST_ASSISTANT_INSTRUCTION = "try to understand what the user is trying to draw (what their gioal is), and only describe it in a maximum of 3 sentences"

THERAPIST_ASSISTANT="You are an online art therapist. Your goal is to help users understand and express their mental and emotional issues through art therapy. Start by asking a series of insightful and compassionate questions to understand the user's current mental and emotional state, their challenges, and any specific issues they are facing. Once you have gathered enough information, transition to a drawing session. Encourage the user to express their feelings, thoughts, and experiences through drawing. Provide gentle guidance and support throughout the process, offering suggestions on techniques and themes they might explore. Aim to create a safe and supportive environment where the user feels comfortable sharing and expressing their inner world through art."

if __name__ == "__main__":
    create_assistant("art_assistant", "gpt-4-turbo", ARTIST_ASSISTANT_INSTRUCTION)
    create_assistant("art_assistant_therapist", "gpt-4-turbo", THERAPIST_ASSISTANT)
