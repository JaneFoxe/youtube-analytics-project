from datetime import timedelta
import os
from googleapiclient.discovery import build
import isodate


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_info = self.get_service().playlists().list(id=self.playlist_id,
                                                            part='snippet',
                                                            ).execute()
        self.info_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                   part='contentDetails, snippet',
                                                                   maxResults=50).execute()
        video_id = []
        for video in self.info_videos['items']:
            video_id.append(video['contentDetails']['videoId'])
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(video_id)).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @classmethod
    def get_service(cls):
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey='AIzaSyAqaKyoG4xvath8iukixy_yDRioZ9c2klk')
        return youtube

    @property
    def total_duration(self):
        result = timedelta()
        for video in self.video_response['items']:
            duration = isodate.parse_duration(video['contentDetails']['duration'])
            result += duration
        return result

    def show_best_video(self):
        if not self.video_response:
            return None
        best_video = max(self.video_response['items'], key=lambda x: x['statistics']['likeCount'])
        return f'https://youtu.be/{best_video["id"]}'
