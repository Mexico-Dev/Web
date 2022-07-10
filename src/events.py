from datetime import datetime, timedelta
import pytz
import requests
import re

class Events:
    __discord_api = "https://discord.com/api/v9"
    __regex = {
        "bold": (r"\*\*(.*?)\*\*", r"<b>\1</b>"),
        "italic": (r"_(.*?)_", r"<i>\1</i>"),
        "code": (r"`(.*?)`", r"<code>\1</code>"),
    }
    
    def __init__(self, guild_id: str, token: str) -> None:
        self.__last_update = datetime.now() - timedelta(minutes=1)
        self.__guild_id = guild_id
        self.__headers = {"authorization": token}
        self.__events = []
    
    @property
    def list(self) -> list:
        self.__updated()
        if self.__events:
            events = []
            for event in self.__events:
                event = {
                    "name": event["name"],
                    "description": self.__markdown(event["description"]),
                    "image": (
                        None,
                        f"https://cdn.discordapp.com/guild-events/{event['id']}/{event['image']}.png?size=4096"
                    )[bool(event["image"])],
                    "start_time": event["scheduled_start_time"],
                    "date": datetime.fromisoformat(event["scheduled_start_time"]).strftime("%d/%m/%Y %H:%M"),
                    "live": datetime.fromisoformat(event["scheduled_start_time"].replace(" ", "")) <= pytz.utc.localize(datetime.now()),
                    "creator": {
                        "name": event["creator"]["username"],
                        "avatar": (
                            None,
                            f"https://cdn.discordapp.com/avatars/{event['creator']['id']}/{event['creator']['avatar']}.png?size=256"
                        )[bool(event['creator']['avatar'])],
                    }
                }
                events.append(event)
            events.sort(key=lambda x: datetime.fromisoformat(x["start_time"]))
            return events
    
        return self.__events
    
    def __markdown(self, text: str) -> str:
        for regex, rep in self.__regex.values():
            text = re.sub(regex, rep, text)
            print(text)
        return text
        
        
    def __updated(self):
        if self.__last_update <= datetime.now():
            self.__events = self.__get_events()
            self.__last_update = datetime.now() + timedelta(minutes=1)
        
    
    def __get_events(self):
        events = requests.get(
            url=f"{self.__discord_api}/guilds/{self.__guild_id}/scheduled-events", 
            headers=self.__headers
        )
        return events.json() if events.status_code == 200 else self.__events