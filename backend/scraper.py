import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys

def get_outstanding_transcripts_for_session(session):
    page_size = 250
    url = f"https://sencanada.ca/en/Committees/NFFN/MeetingSchedule/#?filterSession={session}&CommitteeID=1013&PageSize={page_size}&SortOrder=DATEDESC"

    driver = webdriver.Chrome('chromedriver') # Initiate webdriver
    driver.get(url) 
    time.sleep(5)   # Let the page load
    raw_html = driver.page_source

    soup = BeautifulSoup(raw_html, "html.parser")
    all_transcripts = soup.find_all('a', {'title':'Transcripts'}, href=True)
    all_transcripts = [all_transcripts[x]['href'] for x in range(len(all_transcripts))]
    return all_transcripts

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

# Only for testing purposes
if __name__ == "__main__":
    LATEST_SESSION = '43-2'
    outstanding_transcripts = get_outstanding_transcripts_for_session(LATEST_SESSION)
    for transcript in outstanding_transcripts:
        subsample = get_subsample(transcript, 2)
        print(subsample, len(subsample))