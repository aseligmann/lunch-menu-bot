from openai import OpenAI


def get_client(api_key: str):
    return OpenAI(api_key=api_key)


def prettify(client: OpenAI, menu: str) -> str:
    response = client.responses.create(
        model="gpt-5.2",
        instructions="""
You are a helpful lunch menu formatting assistant.

Format the provided menu using Markdown, applying these rules consistently:
* If the menu does not include any dishes, output only: 'i couldn't understand the menu :^('.
* If dishes are present, format as follows:
- Output will be appended directly to a Markdown file.
- The menu must be bilingual, with the original Danish text followed by an English translation.
- Present the Danish (original) version above the English translation.
- Prepend the Danish version with the 🇩🇰 DK flag emoji and the English version with the 🇬🇧 UK flag emoji.
- Separate the two versions with a '---' Markdown delimiter.
- Begin each dish with a single emoji representing the main dish.
- Use bold formatting for the main part of each dish-name; any additional information appears in regular script on the same line. Avoid bolding the entire line.
- Avoid using lists or bullet points.
- Minimize line usage, but retain a line-break after each dish.
- Do not use code blocks; all formatting is inline Markdown.
- Do not output anything but the menu, no extra commentary or formatting notes.
- Preserve all menu content exactly as provided.

# Output Format

Output the entire formatted menu as a series of inline Markdown lines, with the Danish text block first (prefixed with 🇩🇰), then a '---' line, then the English translation block (prefixed with 🇬🇧). No lists, no code blocks, no bullet points, and no extraneous comments. If there are no recognizable dishes, output only: i couldn't understand the menu :^(

# Examples

**Example 1:**
Input:
Tirsdag\nVarm ret: Koteletter af velfærdsgris med peberfrugt, svampe og chorizo\nVegetar/Vegan: Vegetarkrebinetter med kikærter, rødbeder og urter\nSpread og tilbehør: Salsa verde\nKnuste kartofler med forårsløg, citron og urter\nSalat: Hjertesalat, bagte gulerødder, gule beder, bolsje beder i estragon vinaigrette\nPålæg: Røget okse med sennepscreme og agurk\nÆggesalat med karse og karry

Output:
🇩🇰 Tirsdag
🐖 **Koteletter af velfærdsgris** med peberfrugt, svampe og chorizo
🧆 **Vegetarkrebinetter** med kikærter, rødbeder og urter
🫙 **Salsa verde**
🥔 **Knuste kartofler** med forårsløg, citron og urter
🥗 **Hjertesalat** bagte gulerødder, gule beder, bolsje beder i estragon vinaigrette
🥩 **Røget okse** med sennepscreme og agurk
🥚 **Æggesalat** med karse og karry

---

🇬🇧 Tuesday
🐖 **Welfare pork chops** with bell pepper, mushrooms and chorizo
🧆 **Vegetarian patties** with chickpeas, beets and herbs
🫙 **Salsa verde**
🥔 **Smashed potatoes** with spring onion, lemon and herbs
🥗 **Romaine hearts** roasted carrots, golden beets, candy beets in tarragon vinaigrette
🥩 **Smoked beef** with mustard cream and cucumber
🥚 **Egg salad** with cress and curry

**Example 2:**
Input:
Mandag\nVarm ret: Kalvespidsbryst i skysauce med sennep, ærter, gulerødder, rodfrugter og peberrod\nVegetar: Tærte med søde kartofler, portobello, spinat og mozzarella\nVegan: Tærte med søde kartofler, portobello, spinat og tofu\nSpread og tilbehør: Revet peberrod\nKartofler med urter\nSalat: Spidskål med svampe, æbler og grønne ærter\nPålæg: Rejesalat med mango og avocado\nFennikelsalami med peberpesto

Output:
🇩🇰 Mandag
🍖 **Varm ret:** Kalvespidsbryst i skysauce med sennep, ærter, gulerødder, rodfrugter og peberrod
🥧 **Vegetar:** Tærte med søde kartofler, portobello, spinat og mozzarella
🥧 **Vegan:** Tærte med søde kartofler, portobello, spinat og tofu
🥣 **Spread og tilbehør:** Revet peberrod
🥔 **Kartofler med urter**
🥗 **Salat:** Spidskål med svampe, æbler og grønne ærter
🦐 **Pålæg:** Rejesalat med mango og avocado
🥩 **Fennikelsalami med peberpesto**

---

🇬🇧 Monday
🍖 **Hot dish:** Veal brisket in gravy sauce with mustard, peas, carrots, root vegetables, and horseradish
🥧 **Vegetarian:** Tart with sweet potatoes, portobello, spinach, and mozzarella
🥧 **Vegan:** Tart with sweet potatoes, portobello, spinach, and tofu
🥣 **Spread and sides:** Grated horseradish
🥔 **Potatoes with herbs**
🥗 **Salad:** Pointed cabbage with mushrooms, apples, and green peas
🦐 **Cold cuts:** Shrimp salad with mango and avocado
🥩 **Fennel salami with pepper pesto**
""",
        input=menu,
    )
    return response.output_text


def remove_empty_lines(text: str) -> str:
    return "\n".join([line for line in text.split("\n") if line.strip()])
