import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import time
import uuid

app = FastAPI(title="AI Music Transcriber Online")

# 設定 CORS，允許你的前端網頁從任何地方連線
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 建立臨時目錄
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- 根目錄測試 (確保伺服器活著) ---
@app.get("/")
def read_root():
    return {"status": "Online", "message": "Python Backend is running on Render!"}

# --- API: 上傳與分析 ---
@app.post("/api/upload")
async def upload_audio(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    # 保存檔案到暫存區
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # --- 這裡執行 AI 邏輯 (模擬) ---
    print(f"Processing {file.filename}...")
    time.sleep(2) # 模擬運算時間
    
    # 模擬結果
    simulated_result = {
        "status": "success",
        "job_id": job_id,
        "data": {
            "bpm": 128,
            "key": "C Minor",
            "filename": file.filename
        },
        "note": "這是從雲端 Python 回傳的模擬數據"
    }
    
    # 清理檔案 (因為免費伺服器空間有限)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return simulated_result

@app.post("/api/youtube")
async def process_youtube(url: str = Form(...)):
    return {"status": "success", "data": {"bpm": 120, "key": "Am (Simulated)"}}

if __name__ == "__main__":
    # 本地測試用，上傳雲端後這行不會被執行
    uvicorn.run(app, host="0.0.0.0", port=8000)
