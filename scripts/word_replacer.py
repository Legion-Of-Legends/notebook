import os
import re
from extra_info import member_github_link, status_links



# Precompile regex patterns
pattern_map = {
    re.compile(rf'\b{re.escape(name)}\b'): f'[{name}]({link})'
    for name, link in member_github_link.items()
}

# Directory to scan (change to "." for current)
root_dir = ".."

# Walk through all files in directory and subdirectories
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".md"):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            original_content = content

            # Replace all matches using regex
            for pattern, replacement in pattern_map.items():
                content = re.sub(
                        rf'(?<!\[)({pattern.pattern})(?!\]\()',
                        replacement,
                        content
                        )
            # Only overwrite if something actually changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)

# Replace status links in book_tracker markdown files
status_pattern = {re.compile(rf'\b{re.escape(status)}\b'): link
                  for status, link in status_links.items()}
with open("../Books/README.md", "r", encoding="utf-8") as file:
    content = file.read()
    original_content = content
for pattern, link in status_pattern.items():
    content = re.sub(
        rf'(?<!\!\[)({pattern.pattern})(?!\]\()',
        link,
        content
    )

if content != original_content:
        with open("../Books/README.md", "w", encoding="utf-8") as file:
            file.write(content)
# Setting current members name Current_Members.md
with open("../Current_Members.md", "w", encoding="utf-8") as file:
    file.write("# Current Members\n\n")
    for name in member_github_link.keys():
        file.write(f"- [{name}]({member_github_link[name]})\n")
