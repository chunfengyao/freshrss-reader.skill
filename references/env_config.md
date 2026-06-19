# Environment Configuration & Variables

## Hermes gateway behavior
- **Automatic .env injecting**: Hermes gateway will inject `~/.env` at startup. No manual sourcing required.
- **Limit/Secure**: DO NOT override/read `SELF_HOSTED_FRESHRSS_BASE_URL`, `SELF_HOSTED_FRESHRSS_USERNAME`, `SELF_HOSTED_FRESHRSS_API_KEY` which should injected by Hermes gateway ONLY and should be kept UNTOUCH. `SELF_HOSTED_FRESHRSS_API_KEY` was desensitized by Hermes gateway.

If the script reports missing variables, notify the user to check the following environment variables in `~/.env`.

| Variable | Description | Note |
| :--- | :--- | :--- |
| `SELF_HOSTED_FRESHRSS_BASE_URL` | FreshRSS base URL | |
| `SELF_HOSTED_FRESHRSS_USERNAME` | Login username | |
| `SELF_HOSTED_FRESHRSS_API_KEY` | Login API key / password | Injected by Hermes gateway only, desensitized by Hermes gateway, will always get "***" when read |
| `SELF_HOSTED_FRESHRSS_CATEGORY` | Subscription category name | |
