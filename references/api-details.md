# FreshRSS API & Formatting Details

This document captures the implementation specifics and requirements discovered for this skill.

## Authentication (ClientLogin)
Standard Google Reader API headers are insufficient for this FreshRSS instance.
- **Endpoint**: `{base_url}/api/greader.php/accounts/ClientLogin`
- **Method**: `GET`
- **Parameters**: `Email={username}`, `Passwd={apikey}`
- **Result**: Returns a `text/plain` response in the format `SID=...\nLSID=...\nAuth=...`. Use regex `Auth=(.+)` to extract the token. Some configurations might return JSON, so a fallback is recommended.

## Connection Requirements
- **Timeout**: A `10` second timeout is mandatory for requests to the FreshRSS server, as it is hosted on an internal network and may experience latency.

## Output Formatting (Markdown)
To comply with user preferences for chat-based reporting:
- **Timestamp**: `[MM-DD HH:MM UTC+offset]` (e.g., `[05-09 14:30 UTC+8]`)
- **Title**: Must be **bolded** (`**标题**`).
- **Summary**:
    - Label must be **bolded** (`**摘要:**`).
    - If the summary is extremely long, it must be truncated at approximately 200 characters to maintain readability.
    - HTML tags in the raw summary must be stripped.
