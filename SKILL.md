---
name: freshrss-reader
description: Fetch and formate RSS items in Markdown from FreshRSS.
category: data-source
---

# freshrss-reader

## Description
Fetches the raw RSS items from a specified FreshRSS category via API and outputs them in Markdown style.

## Dependencies
- All dependencies have been installed in `~/workspace/.venv_freshrss-reader` when install this skill.

## Scripts
- [setup.sh](scripts/setup.sh) — create venv and install dependencies required by this skill (for install this skill only.).
- [fetch_data.py](scripts/fetch_data.py) — main script.
  - **DO NOT** call the main script from any python script or code block, or you will get an error that required env was not found.
  - Call the main script through `~/workspace/.venv_freshrss-reader/bin/python` and you will get the output(in Markdown) or error message when script failed.

## Modification Protocol
- **STRICT PERMISSION REQUIREMENT**: Any changes to this skill MUST be explicitly proposed to the user, with the objective clearly explained, and any changes  CANNOT be executed until the user provides express consent.

## References (In the process of task execution, if any issues are encountered, Search/match this reference to see if a solution or constraint already exists after the user has authorized you to proceed.)
- Config: [env_config.md](references/env_config.md)
- Pitfalls: [pitfalls.md](references/pitfalls.md)
- Troubleshooting: [troubleshooting.md](references/troubleshooting.md)
- API Details: [api-details.md](references/api-details.md)
