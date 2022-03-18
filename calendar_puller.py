import logging
import os
from datetime import date, datetime
from pathlib import Path
from urllib.request import urlopen

import pandas as pd
from ics import Calendar
import re

logger = logging.getLogger()
companyA_calendar = "XXXXXprivate-calendar-urlXXXXX"
output = "companyA.csv"

def get_organizer(input):
    pattern = r"CN=([^:]*)"
    result = re.search(pattern, str(input))
    return(result[1])

def read_calendar(url):
    logger.info("Reading calendar")
    cal = Calendar(urlopen(url).read().decode("iso-8859-1"))

    # get events
    events = [e.__dict__ for e in cal.events]
    logger.info(f"Fetched {len(events)} events")
    return events

def prepare_data(company_name, events):
    df = pd.DataFrame(events)

    df.drop('_duration', inplace=True, axis=1)
    df.drop('_begin_precision', inplace=True, axis=1)
    df.drop('_status', inplace=True, axis=1)
    df.drop('_classification', inplace=True, axis=1)
    df.drop('uid', inplace=True, axis=1)
    df.drop('created', inplace=True, axis=1)
    df.drop('last_modified', inplace=True, axis=1)
    df.drop('url', inplace=True, axis=1)
    df.drop('transparent', inplace=True, axis=1)
    df.drop('alarms', inplace=True, axis=1)
    df.drop('attendees', inplace=True, axis=1)
    df.drop('categories', inplace=True, axis=1)
    df.drop('_geo', inplace=True, axis=1)
    df.drop('extra', inplace=True, axis=1)
    df.drop('_classmethod_args', inplace=True, axis=1)
    df.drop('_classmethod_kwargs', inplace=True, axis=1)

    #add the date column
    df.insert(0, column = "end_date", value="")  
    df['end_date'] = df['_begin']
    df.insert(0, column = "start_date", value="")  
    df['start_date'] = df['_end_time']

    for index, row in df.iterrows():
        row['start_date'] = row['start_date'].date().strftime("%d-%m-%Y")
        row['end_date'] = row['end_date'].date().strftime("%d-%m-%Y")
        row['_begin'] = row['_begin'].time().strftime("%H:%M")
        row['_end_time'] = row['_end_time'].time().strftime("%H:%M")
        row['organizer'] = get_organizer(row['organizer'])
    
    
    # dump outputfile
    outputfile = Path(company_name)
    logger.info(f"Saving to {output}")
    df.to_csv(outputfile, index=False)
    logger.info("====CSV Ready====")
    return outputfile


def interview_now(output_filename, url):
    # get calendar
    if not url:
        logger.error("URL argument or CAL_ICS_URL env variable must be set")
        quit()

    events = read_calendar(url)

    prepared_file = prepare_data(output_filename,events)
    
    return
    


if __name__ == "__main__":
    logging.basicConfig(filename='myapp.log', format='%(asctime) s %(message) s', level=logging.INFO)
    logger.info("====New Start====")
    interview_now(output, companyA_calendar)