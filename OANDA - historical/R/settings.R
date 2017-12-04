#   Settings for OANDA API script

ENVIRONMENTS <- list(
					"streaming"= list(
									"real"= "stream-fxtrade.oanda.com",
									"practice"= "stream-fxpractice.oanda.com"
					),
					"api"= list(
								"real"= "api-fxtrade.oanda.com/",
								"practice"= "api-fxpractice.oanda.com"
					)
)

DOMAIN <- "real"
STREAM_DOMAIN <- ENVIRONMENTS[["streaming"]][[DOMAIN]]
API_DOMAIN <- ENVIRONMENTS[["api"]][[DOMAIN]]

ACCESS_TOKEN <- Sys.getenv("ACC_TOKEN")
ACCOUNT_ID <- Sys.getenv("ACC_ID")
