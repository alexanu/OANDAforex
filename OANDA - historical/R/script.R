#
#
#   Script v0.1 for OANDA API
#
##############################################################################
# Load settings
##############################################################################
setwd("/path/to/home")


relib <- function(){
    source("settings.R")
    source("functions.R")
}
relib()

#----------------------------------------

# "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&
#  start=2014-06-19T15%3A47%3A40Z
#  &end=2014-06-19T15%3A47%3A50Z"


getprices <- function(startdate, enddate, instrument){
    path <- "v1/candles"
    query <- list(
        instrument=instrument,
        start=startdate,    
        end=enddate,        
        granularity="M10",
        includeFirst="false"
    )
    url <- modify_url( url=paste0( "https://", API_DOMAIN), path=path, query=query)
    
    # check access credentials have been set in env var
    if (identical(Sys.getenv("ACC_TOKEN"), "")) {
        stop("Please set your access token", call. = FALSE)
    }
    if (identical(Sys.getenv("ACC_ID"), "")) {
        stop("Please set your account ID", call. = FALSE)
    }
    
    headers <- paste0("Authorization: Bearer ", ACCESS_TOKEN)
    GET(url, add_headers(headers), verbose(info=TRUE) )
}

# get the hisorical prices
resp <- getprices( instrument="GBP_JPY", 
                   startdate="2017-08-10T00:00:00",
                   enddate="2017-08-10T01:00:00")

# check for response errors
if(resp$status_code != 200){
    cat( "\n[+] Error   ->   Status code:", resp$status_code, "\n\n") 
    
}
if(http_type(resp) != "applicatio/json"){
    cat( "\n[+] Error   ->   Server did not respond with JSON object")
    cat( "\n\t\t\t Response:", http_type(resp), "\n\n" )
}

parsed <- fromJSON( content( resp, "text"))[["candles"]]







