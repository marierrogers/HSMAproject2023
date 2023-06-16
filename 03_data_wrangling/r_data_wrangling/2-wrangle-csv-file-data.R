# Wrangle the CSV files

library(tidyverse)

monthly_csv <- list.files('tempdir')[grepl('monthly', tolower(list.files('tempdir')))]
annual_csv <- list.files('tempdir')[grepl('annual', tolower(list.files('tempdir')))]

annual_df <- read_csv(paste0('tempdir/',annual_csv))
monthly_df <- read_csv(paste0('tempdir/',monthly_csv))

js_df <- readRDS('tempdir/inactive_organisations.rds')

process_turnover_df <- function(df) {
  df1 <- df %>%
    mutate(
      date_string = case_when(
        (Type %in% c('Leavers', 'Joiners')) ~ paste0(str_extract(Period, "[^ to ]+$"),'01'),
        Type == 'Denoms' ~ paste0('01/',str_sub(Period, 4, 10)),
        TRUE ~ NA_character_
      ),
      thedate = as.Date(lubridate::now())
    )
  
  # Convert strings to dates, depending on which Type it is
  # Bit of a fudge, but I can't get it to work in the mutate statement
  df1$thedate[df1$Type == 'Denoms'] = parse_date(df1$date_string[df1$Type == 'Denoms'], format = '%d/%m/%Y')
  df1$thedate[df1$Type != 'Denoms'] = parse_date(df1$date_string[df1$Type != 'Denoms'], format = '%Y%m%d')
  
  #print(df1 %>% count(`Org code`, `Staff group`, thedate))
  
  df2 <- df1 %>%
    group_by(`Org code`, `Staff group`, thedate) %>%
    transmute(
      n = n(),
      join_HC = if (any(Type == 'Joiners')) {HC[Type == 'Joiners']} else {NA},
      join_FTE = if (any(Type == 'Joiners')) {FTE[Type == 'Joiners']} else {NA},
      leave_HC = if (any(Type == 'Leavers')) {HC[Type == 'Leavers']} else {NA},
      leave_FTE = if (any(Type == 'Leavers')) {FTE[Type == 'Leavers']} else {NA},
      denom_HC = if (any(Type == 'Denoms')) {HC[Type == 'Denoms']} else {NA},
      denom_FTE = if (any(Type == 'Denoms')) {FTE[Type == 'Denoms']} else {NA},
    ) %>% ungroup() %>% 
    rename(
      org_code = `Org code`,
      staff_group = `Staff group`,
      month_year = thedate
    ) %>% distinct()
  
  return(df2)

}

# Annual data
processed_annual_df <- process_turnover_df(annual_df) 
processed_annual_df %>% count() # 251814

processed_annual_df1 <- processed_annual_df %>% anti_join(js_df, by=c("org_code" = "org_id"))
processed_annual_df1 %>% count() # 214839

write_csv(processed_annual_df1, 'tempdir/processed_annual_data.csv')

# Monthly data
processed_monthly_df <- process_turnover_df(monthly_df) 
processed_monthly_df %>% count() # 188936

processed_monthly_df1 <- processed_monthly_df %>% anti_join(js_df, by=c("org_code" = "org_id"))
processed_monthly_df1 %>% count() # 170304

write_csv(processed_monthly_df1, 'tempdir/processed_monthly_data.csv')
