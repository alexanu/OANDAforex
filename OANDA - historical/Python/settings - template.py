ENVIRONMENTS = {
    "streaming": {
        "real": "stream-fxtrade.oanda.com",
        "practice": "stream-fxpractice.oanda.com",
        "sandbox": "stream-sandbox.oanda.com"
    },
    "api": {
        "real": "api-fxtrade.oanda.com",
        "practice": "api-fxpractice.oanda.com",
        "sandbox": "api-sandbox.oanda.com"
    }
}

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]

#Enter API token
ACCESS_TOKEN = 'token-as-string'
# or from environment variable
#ACCESS_TOKEN = os.environ.get('OANDA_API_ACCESS_TOKEN', None)

#Enter the account ID
ACCOUNT_ID = 'ID-as-string'
# or from environment variable
#ACCOUNT_ID = os.environ.get('OANDA_API_ACCOUNT_ID', None)

