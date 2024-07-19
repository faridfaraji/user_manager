from openai import OpenAI

client = OpenAI()


def get_latest_file(thread_id, filename):
    thread_messages = client.beta.threads.messages.list(thread_id)
    for msg in thread_messages.data:
        for itm in msg.content:
            if itm.type == "image_file":
                itm.image_file.file_id
                content = client.files.content(itm.image_file.file_id)
                with open(filename, 'wb') as f:
                    f.write(content.content)
                return

