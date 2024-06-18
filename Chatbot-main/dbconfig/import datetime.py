import datetime
from ics import Calendar, Event
import requests
from bs4 import BeautifulSoup

# Function to fetch video titles from a YouTube playlist
def fetch_youtube_playlist_titles(playlist_url):
    response = requests.get(playlist_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract video titles
    video_titles = [video.get_text().strip() for video in soup.find_all('a', {'class': 'pl-video-title-link'})]
    return video_titles

# Sample YouTube playlist URL
playlist_url = "https://www.youtube.com/playlist?list=PLSDeUiTMfxW6VChKWb26Z_mPR4f6fAmMV"
video_titles = fetch_youtube_playlist_titles(playlist_url)

# Initialize the start date
start_date = datetime.datetime(2024, 6, 16)

# Define time slots
time_slots = [
    (datetime.time(16, 0), datetime.time(20, 0)),
    (datetime.time(22, 0), datetime.time(23, 30))
]

# Create a calendar
calendar = Calendar()

# Populate the calendar with events
day = 0
for title in video_titles:
    for start_time, end_time in time_slots:
        event_date = start_date + datetime.timedelta(days=day)
        event_start = datetime.datetime.combine(event_date, start_time)
        event_end = datetime.datetime.combine(event_date, end_time)
        
        event = Event()
        event.name = f"Day {day + 1}: {title}"
        event.begin = event_start.isoformat()
        event.end = event_end.isoformat()
        event.description = f"Watch video: {title}\nLink: {playlist_url}"
        
        calendar.events.add(event)
        day += 1
        if day >= 100:
            break
    if day >= 100:
        break

# Save the calendar to an .ics file
ics_file_path = "youtube_playlist_schedule.ics"
with open(ics_file_path, 'w') as f:
    f.writelines(calendar)
