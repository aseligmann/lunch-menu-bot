import requests
from lunch_menu_bot.time.time import Day
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_menu_page():
    """
    Fetch the menu from the website.
    """
    logger.info("Fetching the menu...")
    # Fetch the menu from the website

    url = "https://kragerupogko.dk/ugemenuer/"
    response = requests.get(url)
    html_content = response.text

    logger.info("Finished fetching the menu.")
    return html_content


def parse_menu_page(html_content, column_identifier):
    logger.info("Starting to parse the menu.")
    if html_content is None:
        logger.warning("No HTML content found.")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all div element with data-element_type="column"
    columns = soup.find_all("div", {"data-element_type": "column"})
    if columns is None:
        logger.warning("No columns found with data-element_type='column'.")
        return None
    logger.debug(f"Found {len(columns)} columns.")

    # Select the column which contains week_str
    week_menu_column = None
    for column in columns:
        if column_identifier.lower() in column.get_text().lower():
            week_menu_column = column
            logger.info(
                f"Found column containing the specified identifier: {column_identifier}"
            )
            break

    if not week_menu_column:
        logger.warning("No column found containing the specified identifier.")
        return None

    # Extract all <p> elements from the deepest divs
    p_elements = week_menu_column.find_all("p")
    logger.info(f"Found {len(p_elements)} <p> elements in the week menu column.")

    # Construct menu dictionary
    menu = {
        Day.MONDAY: None,
        Day.TUESDAY: None,
        Day.WEDNESDAY: None,
        Day.THURSDAY: None,
        Day.FRIDAY: None,
    }
    n_p_elements = len(p_elements)
    for i, paragraph in enumerate(p_elements):
        # Extract text from each <p> element, replace <br> with newline, and store in a list
        paragraph_text = paragraph.get_text(separator="\n", strip=True)

        # Store the menu for each day in the menu dictionary
        for day in Day:
            if day.value.lower() in paragraph_text.lower():
                menu[day] = paragraph_text
                logger.info(f"Paragraph {i+1}/{n_p_elements}: Found menu for {day}...")
                break
        else:
            logger.debug(
                f"Paragraph {i+1}/{n_p_elements}: No day found in the paragraph text."
            )

    logger.info(
        f"Did not find any menu for the following days: {[day for day, text in menu.items() if text is None]}"
    )
    logger.info("Finished parsing the menu.")

    return menu


if __name__ == "__main__":
    from lunch_menu_bot.time.time import get_week_and_day

    with open("menu.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    week_number, day = get_week_and_day()
    column_identifier = f"Uge {week_number}"
    menu = parse_menu_page(html_content, column_identifier)
    if menu is None:
        print("No menu found")
        exit()

    day = Day.FRIDAY

    if day not in menu:
        print("No menu found for today")
        exit()

    print(menu[day])
