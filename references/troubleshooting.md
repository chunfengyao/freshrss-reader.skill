# Troubleshooting FreshRSS Auth (401)

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
