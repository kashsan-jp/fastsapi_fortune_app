import json
from typing import List, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5501",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジン（"*"で全て許可も可能）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSONファイルのパス
DATA_FILE = "fortuneData.json"

# データ構造を定義するPydanticモデル
class Item(BaseModel):
    id: int
    star: str
    character: str

# ユーティリティ関数: JSONの読み込み
def load_json() -> List[Any]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ユーティリティ関数: JSONの書き込み
def save_json(data: List[Any]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# GET: JSONファイルの全データを取得
@app.get("/items", response_model=List[Item])
def get_items():
    return load_json()

# POST: 新規データを追加してJSONファイルに保存
@app.post("/items", response_model=Item)
def create_item(item: Item):
    data = load_json()
    
    # IDの重複チェック
    if any(i["id"] == item.id for i in data):
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    # データを追加して保存
    data.append(item.model_dump())
    save_json(data)
    
    return item
