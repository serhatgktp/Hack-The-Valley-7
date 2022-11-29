import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import mysql_utils as mu

def get_outstanding_transcripts_for_session(session, config, table_name):
    page_size = 250
    url = f"https://sencanada.ca/en/Committees/NFFN/MeetingSchedule/#?filterSession={session}&CommitteeID=1013&PageSize={page_size}&SortOrder=DATEDESC"

    driver = webdriver.Chrome('chromedriver') # Initiate webdriver
    driver.get(url) 
    time.sleep(5)   # Let the page load
    raw_html = driver.page_source

    soup = BeautifulSoup(raw_html, "html.parser")
    transcripts = soup.find_all('a', {'title':'Transcripts'}, href=True)
    transcripts = [transcripts[x]['href'] for x in range(len(transcripts))]
     
    existing_transcripts = mu.load_as_df(config, table_name)
    if existing_transcripts is not None:
        existing_transcripts = existing_transcripts["reference"].tolist()
        for transcript in transcripts:
            if transcript in existing_transcripts:
                transcripts.remove(transcript)
    return transcripts

def get_subsamples(transcript, breadth=3):
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