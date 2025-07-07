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
                "content": ""
                + "Make this menu pretty by formatting beautifully as markdown. "
                + "If the menu does not contain any dishes, then ignore all the following instructions and do not output any menu. "
                + "Instead output a message saying 'i couldn't understand the menu :^('. "
                + "If the menu contains any dishes, then output the menu according to the instructions below. "
                + "Your output will be appended directly to a markdown file. "
                + "Put the main part of the dish in bold, and the rest in normal script. "
                + "Add a single emoji at the beginning of each line, associated with the main dish described on the line. "
                + "Afterwards, output it both in Danish (original) and translated to English. "
                + "Add a delimiter between the two versions. "
                + "Add a DK flag emoji 🇩🇰 before the danish version and a UK flag emoji 🇬🇧 before the english version. "
                + "Don't use bullets or lists, and try to keep the line count low. "
                + "DO NOT PUT THE TEXT INSIDE A CODE BLOCK, KEEP IT AS INLINE MARKDOWN. "
                + "DO NOT OUTPUT ANYTHING OTHER THAN THE MENU. "
                + "Make very sure not to change any of the menu content! "
                + "The menu is as follows:\n\n"
                + menu,
            },
        ],
    )
    # Return only the new string
    return completion.choices[0].message.content


def remove_empty_lines(text: str) -> str:
    return "\n".join([line for line in text.split("\n") if line.strip()])
