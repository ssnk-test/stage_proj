import httpx


class MonServiceAPI:
    def __init__(self):
        self.host = "mon_service"
        self.port = "8082"
        self.path = ""

    async def add_event(self, body):
        url = f"http://{self.host}:{self.port}{self.path}/events"

        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, json=body)
        return r.json()

    async def view_events(self):
        url = f"http://{self.host}:{self.port}{self.path}/events"
        async with httpx.AsyncClient() as ac:
            r = await ac.get(url)
        return r.json()
