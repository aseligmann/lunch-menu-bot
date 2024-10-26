from openai import OpenAI


def get_client(api_key: str):
    return OpenAI(api_key=api_key)


def prettify(client: OpenAI, menu: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Make this menu pretty by formatting beautifully as markdown and adding an emoji each dish and for each ingredient. "
                + "Don't use bullets or lists, and try to keep the line count low. "
                + "Afterwards, output it both in Danish (original) and translated to English. "
                + "Add a delimiter between the two versions. "
                + "Add a DK flag emoji 🇩🇰 before the danish version and a UK flag emoji 🇬🇧 before the english version. "
                + "Make very sure not to change any of the content! "
                + "DO NOT OUTPUT ANYTHING OTHER THAN THE MENU. "
                + "The menu is as follows:\n\n"
                + menu,
            },
        ],
    )
    # Return only the new string
    return completion.choices[0].message.content


def remove_empty_lines(text: str) -> str:
    return "\n".join([line for line in text.split("\n") if line.strip()])
