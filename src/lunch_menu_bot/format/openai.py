from openai import OpenAI


def get_client(api_key: str):
    return OpenAI(api_key=api_key)


def prettify(client: OpenAI, menu: str) -> str:
    response = client.responses.create(
        model="gpt-5.1",
        instructions=""
        + "You are a helpful lunch menu formatting assistant.\n"
        + "Format the provided menu using Markdown, applying these rules consistently:\n"
        + "- If the menu does not include any dishes, output only: 'i couldn't understand the menu :^('.\n"
        + "- If dishes are present, format as follows:\n"
        + "  - Output will be appended directly to a Markdown file.\n"
        + "  - Present the Danish (original) version above the English translation.\n"
        + "  - Prepend the Danish version with the 🇩🇰 DK flag emoji and the English version with the 🇬🇧 UK flag emoji.\n"
        + "  - Separate the two versions with a '---' Markdown delimiter.\n"
        + "  - Begin each dish with a single emoji representing the main dish.\n"
        + "  - Use bold formatting for the main part of each dish-name; any additional information appears in regular script on the same line. Avoid bolding the entire line.\n"
        + "  - Avoid using lists or bullet points.\n"
        + "  - Minimize line usage, but retain a line-break after each dish.\n"
        + "  - Do not use code blocks; all formatting is inline Markdown.\n"
        + "  - Do not output anything but the menu, no extra commentary or formatting notes.\n"
        + "  - Preserve all menu content exactly as provided.",
        input=menu,
    )
    return response.output_text


def remove_empty_lines(text: str) -> str:
    return "\n".join([line for line in text.split("\n") if line.strip()])
