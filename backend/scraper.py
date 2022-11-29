import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import configparser
import mysql_utils as mu
import pandas as pd

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

def get_outstanding_transcripts_for_session(session, config):
    page_size = 250
    url = f"https://sencanada.ca/en/Committees/NFFN/MeetingSchedule/#?filterSession={session}&CommitteeID=1013&PageSize={page_size}&SortOrder=DATEDESC"

    driver = webdriver.Chrome('chromedriver') # Initiate webdriver
    driver.get(url) 
    time.sleep(5)   # Let the page load
    raw_html = driver.page_source

    soup = BeautifulSoup(raw_html, "html.parser")
    transcripts = soup.find_all('a', {'title':'Transcripts'}, href=True)
    transcripts = [transcripts[x]['href'] for x in range(len(transcripts))]
     
    existing_transcripts = mu.load_as_df(config, "transcripts")
    if existing_transcripts is not None:
        existing_transcripts = existing_transcripts["reference"].tolist()
        for transcript in transcripts:
            if transcript in existing_transcripts:
                transcripts.remove(transcript)
    return transcripts

def get_subsample(transcript, breadth=3):
    '''
    Returns a subsample of sentences from the selected transcript

    params:
        page: an html page provided from the chrome driver.
        transcripts: number of transcripts you want returned, if not specified it returns all
    '''

    url = f"https://sencanada.ca{transcript}"
    content = requests.get(url)
    parser = BeautifulSoup(content.content, "html.parser")

    median = len(parser.findAll('p')) // 2

    samples = []
    for i in range(median - breadth, median + breadth):
        samples.append(parser.findAll('p')[i].text)
    return samples

def upload_transcripts_to_db(session, transcripts):
    d = [{'reference':x} for x in transcripts]
    df = pd.DataFrame(d)
    df.insert(column='session', loc=df.shape[1], value=session)
    print(df)
    mu.insert(config, 'transcripts', df)

# Only for testing purposes
if __name__ == "__main__":
    LATEST_SESSION = '43-2'
    outstanding_transcripts = get_outstanding_transcripts_for_session(LATEST_SESSION, config)[:5]
    upload_transcripts_to_db(LATEST_SESSION, outstanding_transcripts)
    print(outstanding_transcripts)
    for transcript in outstanding_transcripts:
        subsample = get_subsample(transcript, 2)
        # print(subsample, len(subsample))