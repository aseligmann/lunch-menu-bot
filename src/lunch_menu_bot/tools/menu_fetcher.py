# Or fetching from a URL (make sure you have permission)
import requests

url = "https://kragerupogko.dk/ugemenuer/"
response = requests.get(url)
html_content = response.text

with open("menu.html", "w", encoding="utf-8") as file:
    file.write(html_content)
