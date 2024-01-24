import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title: str = self.print_info()['snippet']['title']
        self.description: str = self.print_info()['snippet']['description']
        self.url: str = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count: int = self.print_info()['statistics']['subscriberCount']
        self.video_count: int = self.print_info()['statistics']['videoCount']
        self.view_count: int = self.print_info()['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        # print(json.dumps(self.channel, indent=2, ensure_ascii=False))
        channel = self.channel['items'][0]
        return channel

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @classmethod
    def get_service(cls) -> object:
        """Возвращает объект для работы с API."""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def to_json(self, file_name: str) -> None:
        """Сохранить данные в файл."""
        channel_info = {'channel_id': self.channel_id, 'title': self.title, 'description': self.description,
                        'url': self.url, 'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                        'view_count': self.view_count}
        with open(file_name, 'w', encoding='utf=8') as f:
            json.dump(channel_info, f, ensure_ascii=False)
