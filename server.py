from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import pyautogui
import zlib
import io
import json
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mss import mss
from PIL import Image
import asyncio

app = FastAPI()

screen_size = 0.5  # 스크린샷 크기 비율

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://crowdsourcedcloudgaming.netlify.app"],  # 신뢰할 수 있는 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 클라이언트 연결 관리
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.get("/screenshot")
async def get_screenshot():
    """비동기로 스크린샷 캡처 및 전송"""
    compressed_data = await capture_and_compress()
    return StreamingResponse(io.BytesIO(compressed_data), media_type="application/octet-stream")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket을 통한 입력 명령 수신"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                command = json.loads(data)
                process_command(command)
            except json.JSONDecodeError:
                await websocket.send_text("Invalid JSON format")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")


async def capture_and_compress():
    """비동기적으로 스크린샷 캡처 및 zlib 압축"""
    def blocking_capture():
        with mss() as sct:
            monitor = sct.monitors[1]  # 첫 번째 모니터
            screenshot = sct.grab(monitor)  # 스크린샷 캡처
            image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            # 압축 및 리사이즈
            buffer = io.BytesIO()
            width, height = int(image.width * screen_size), int(image.height * screen_size)
            image.resize((width, height)).save(buffer, format="WEBP", quality=85)
            return zlib.compress(buffer.getvalue())

    return await asyncio.to_thread(blocking_capture)


def process_command(command: dict):
    """수신된 명령을 처리"""
    command_type = command.get("type")
    if command_type == "mouse_move":
        pyautogui.moveTo(command["x"], command["y"])
    elif command_type == "mouse_left_down":
        pyautogui.mouseDown(command["x"], command["y"], button="left")
    elif command_type == "mouse_left_up":
        pyautogui.mouseUp(command["x"], command["y"], button="left")
    elif command_type == "mouse_right_down":
        pyautogui.mouseDown(command["x"], command["y"], button="right")
    elif command_type == "mouse_right_up":
        pyautogui.mouseUp(command["x"], command["y"], button="right")
    elif command_type == "key_press":
        pyautogui.press(command["key"])
    else:
        print("Unknown command:", command)

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=443,  # HTTPS 기본 포트
        ssl_keyfile="",  # SSL 키 파일 경로
        ssl_certfile=""  # SSL 인증서 파일 경로
    )
