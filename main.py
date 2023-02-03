from typing import List
from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from tempfile import TemporaryDirectory
import tempfile

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file_received: List[UploadFile]):
    with TemporaryDirectory(prefix="static-") as tmpdir:
        emotions = dict()

        for file in file_received:
            new_file_path = tmpdir + "/" + file.filename

            with open(new_file_path, 'wb') as file_saved:
                file_saved.write(file.file.read())

            emotions.update({file.filename: "works"})

        return {"results": emotions}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        binary_data = await websocket.receive_bytes()
        # Convert binary data to SpooledTemporaryFile
        file = tempfile.NamedTemporaryFile(
            max_size=1000000, mode="wb")
        file.write(binary_data)
        file.seek(0)

        with TemporaryDirectory(prefix="static-") as tmpdir:
            new_file_path = tmpdir + "/" + file.name

            with open(new_file_path, 'wb') as file_saved:
                file_saved.write(file.read())

            result = "works"
            await websocket.send_text(f"Message text was sent: " + result)
