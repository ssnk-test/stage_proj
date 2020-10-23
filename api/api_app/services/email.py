import httpx


class EmailServiceAPI:
    def __init__(self):
        self.host = "email_service"
        self.port = "8081"
        self.path = ""

    async def add(self, body):
        url = f"http://{self.host}:{self.port}{self.path}/templates"
        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, json=body)
        return r.json()

    async def view(self):
        url = f"http://{self.host}:{self.port}{self.path}/templates"
        async with httpx.AsyncClient() as ac:
            r = await ac.get(url)
        return r.json()
