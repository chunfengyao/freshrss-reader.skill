# Pitfalls and Troubleshooting

## Asking FIRST
- If any error occured when executing py script, do nothing and notify the user with error info to handle it.

## Duplicate Articles
- The script now automatically deduplicates articles based on title. If the same article appears multiple times in the feed, only the first occurrence is displayed.

## API Request Limits
- If returning entries are too few, confirm the `n` parameter in `fetch_news` is set large enough (default: 1000).