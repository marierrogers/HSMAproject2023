library(tidyverse)
library(rvest)
library(jsonlite)

# Check tempdir exists

if(!dir.exists('tempdir')) {
  dir.create('tempdir')
}


# Fetch source data

check_url <- 'https://digital.nhs.uk/data-and-information/publications/statistical/nhs-workforce-statistics'
file_source_url <- 'https://digital.nhs.uk'

source_site <- read_html(check_url) %>% html_elements('#past-publications')

a <- source_site %>% html_elements("a") %>% html_attr('href')

# This function will take a given URL string, check if it should
# be included, based on the base URL and if so, return
# the URL and the date
retrieve_stats_URLs <- function(url_string, base_url_string = "publications/statistical/nhs-workforce-statistics") {
  if(grepl(base_url_string, url_string)) {
    x <- str_split(url_string, '/')
    date_string <- tail(x[[1]], 1)
    date_string_as_date <- lubridate::my(date_string)
    #print(date_string_as_date)
    if(!is.na(date_string_as_date)) {
      #print(date_string_as_date)
      return(list(orig_url = url_string, thedate = date_string_as_date))
    }
    
  }
}

# Iterate through webpage and retrieve URLs
# Since we'll also get the date, we can find the most recent
stats_df <- a |> map_dfr(\(a) retrieve_stats_URLs(a, base_url_string = "publications/statistical/nhs-workforce-statistics"))

stats_df %>% glimpse()

web_page_for_data <- paste0(file_source_url, stats_df %>% arrange(desc(thedate)) %>% head(n = 1) %>% pull(orig_url))

fetch_zip_urls <- read_html(web_page_for_data) %>% html_elements('a') %>% html_attr('href')

# Remove contents from tempdir
unlink('tempdir/*.csv')
unlink('tempdir/*.zip')

zip_url <- fetch_zip_urls[grepl('.zip',fetch_zip_urls) & grepl('turnover', tolower(fetch_zip_urls))]

# Download zip file
download.file(
  zip_url,
  "tempdir/turnover.zip",
  mode = "wb"
)

# Unzip files to tempdir
unzip('tempdir/turnover.zip', exdir = 'tempdir')


# Retrieve list of inactive organisations, which will be removed from the time series data ------

js <- read_json('https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?Status=Inactive&Roles=RO197,RO98&Limit=1000', simplifyVector = T)

js_df <- tibble(
  name = js$Organisations$Name,
  org_id = js$Organisations$OrgId
)

saveRDS(js_df, 'tempdir/inactive_organisations.rds')

