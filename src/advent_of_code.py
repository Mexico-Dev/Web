from datetime import datetime
import requests
import asyncio


class Leaderboard:
    __to_init = f"{datetime.now().year}/11/30 00:00"
    __to_finish = f"{datetime.now().year}/12/24 00:00"

    def __init__(self, api: str, cookie: str) -> None:
        self.__advent_of_code_api = api
        self.__cookie = cookie

    @property
    def table(self) -> dict | datetime:
        if self.__to_init <= datetime.now().strftime("%Y/%m/%d %H:%M") <= self.__to_finish:
            leaderboard = asyncio.run(self.get_leaderboard())
            if leaderboard:
                table = {
                    "event": leaderboard["event"],
                    "members": [
                        {
                            "name": member["name"],
                            "stars": int(member["stars"]),
                            "score": member["local_score"],
                        }
                        for member in leaderboard["members"].values()]
                }
                return table
            return {}
        return datetime.strptime(self.__to_init, "%Y/%m/%d %H:%M")

    async def get_leaderboard(self) -> dict:
        leaderboard = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(
            self.__advent_of_code_api,
            cookies={"session": self.__cookie}
        ))
        return leaderboard.json() if leaderboard.status_code == 200 else None
