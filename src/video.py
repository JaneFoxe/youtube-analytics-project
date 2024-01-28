from googleapiclient.discovery import build
import os


class Video:
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        try:
            self.video_id = video_id
            self.video_title: str = self.print_info()['items'][0]['snippet']['title']
            self.video_url: str = 'https://www.youtube.com/channel/' + self.video_id
            self.view_count: int = self.print_info()['items'][0]['statistics']['viewCount']
            self.like_count: int = self.print_info()['items'][0]['statistics']['likeCount']
        except (IndexError, ValueError, KeyError):
            self.video_title = None
            self.video_url = None
            self.like_count = None
            self.view_count = None
            self.video_result = None
            print(f'Видео с id:{self.video_id} не обнаруженно, попробуйте другой id')

    def __str__(self):
        return self.video_title


    def print_info(self):
        """
        Выводит всю информацию о видео в json-формате
        :return: массив информации о видео
        """
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
        return video_response


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

