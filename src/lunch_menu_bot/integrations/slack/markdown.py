import re

REGEX_REPLACE = (
    (re.compile("^- ", flags=re.M), "• "),
    (re.compile("^  - ", flags=re.M), "  ◦ "),
    (re.compile("^    - ", flags=re.M), "    ⬩ "),  # ◆
    (re.compile("^      - ", flags=re.M), "    ◽ "),
    (re.compile("^#+ (.+)$", flags=re.M), r"*\1*"),
    (re.compile(r"\*\*"), "*"),
)


def markdown_to_slack(text: str) -> str:
    for regex, replacement in REGEX_REPLACE:
        text = regex.sub(replacement, text)
    return text
