import os

_GITHUB_SETTING_SITE = 'https://github.com/settings/tokens'

TOKEN = os.environ.get('GITHUB_API_TOKEN')
if TOKEN is None:
    message = 'requires Personal access tokens. '
    message += 'export GITHUB_API_TOKEN="***", '
    message += f'get from {_GITHUB_SETTING_SITE} if you do not have'
    raise RuntimeError(message)

HEADERS = {
    'Authorization': f'token {TOKEN}'
}
