import configparser
import parliament_scraper as pscraper
import summarizer
import pandas as pd
import mysql_utils as mu

# Database Settings
config = configparser.ConfigParser()
config.read('db_config.ini')

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
db = config['mysql']['db']

config = {
    'host': host,
    'user': user,
    'password': password,
    'db': db
}

def upload_summary_to_db(config, session, transcript, summary, table_name):
    d = [{'session':session,'reference':transcript, 'summary':summary}]
    df = pd.DataFrame(d)
    print(df)
    mu.insert(config, table_name, df)

# Only for testing purposes
if __name__ == "__main__":
    LATEST_SESSION = '43-2'
    SUBSAMPLE_BREADTH = 2
    TABLE_NAME = "summaries"

    outstanding_transcripts = pscraper.get_outstanding_transcripts_for_session(LATEST_SESSION, config, TABLE_NAME)
    print("outstanding_transcripts:\n", outstanding_transcripts, len(outstanding_transcripts), '\n- - - - -')
    for transcript in outstanding_transcripts:
        transcript_subsamples = pscraper.get_subsamples(transcript, 2)
        transcript_summary = summarizer.get_summary_of_samples(transcript_subsamples)
        print(transcript_summary)
        upload_summary_to_db(config, LATEST_SESSION, transcript, transcript_summary, TABLE_NAME)
        # print(subsample, len(subsample))