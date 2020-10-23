from api_app.main import get_app
import time
from datetime import datetime
from fastapi import Request, Response
from api_app.services.monitoring import MonServiceAPI

app = get_app()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(dict(request))
    start_time = datetime.now().isoformat()#time.time()
    response = await call_next(request)
    #process_time = time.time() - start_time
    end_time = datetime.now().isoformat()
    a = MonServiceAPI()
    event = {
        "service": (request.url.path).split('/')[1],
        "url": request.url.path,
        "status": str(response.status_code),
        "req_time": str(start_time),
        "res_time": str(end_time)}
    r = await a.add_event(event)

    return response
