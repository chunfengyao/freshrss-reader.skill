# Troubleshooting and Pitfalls

(If any error occurs or modification is needed, search this section FIRST.)

## Error Codes
| Exit Code | Description |
| :--- | :--- |
| -1 | 缺失必要的环境变量 (配置未设置) |
| -2 | 认证失败 (用户名/API Key 错误或 API 不可用) |
| -3 | 获取数据失败 (网络超时或接口调用错误) |

## Authentication (401)
If the script fails with `401 Unauthorized`:

1. **API Key vs. Password**: FreshRSS's Google Reader API compatibility often requires the **API KEY** (found in "Subscription -> API" settings in the FreshRSS web UI), not the account's primary login password.
2. **Endpoint Validation**: The script uses the legacy Google Reader API (`/api/greader.php/accounts/ClientLogin`). Ensure this is enabled in the target FreshRSS instance settings.
3. **Manual Verification**: Use `curl` to verify credentials when troubleshooting:
   ```bash
   curl -G "https://<BASE_URL>/api/greader.php/accounts/ClientLogin" \
     --data-urlencode "Email=<USERNAME>" \
     --data-urlencode "Passwd=<API_KEY>"
   ```
   If it returns `Unauthorized!`, the credentials are invalid for this API.

## Common Issues (Pitfalls)

### Duplicate Articles
- The script automatically deduplicates articles based on title. If the same article appears multiple times in the feed, only the first occurrence is displayed.

### API Request Limits
- If returning entries are too few, confirm the `n` parameter in `fetch_news` is set large enough (default: 1000).
