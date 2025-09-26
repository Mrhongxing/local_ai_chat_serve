from fastapi import FastAPI
from fastapi import HTTPException
import httpx
#uvicorn serve:app --reload运行文件
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",    # 前端开发服务器
        "http://127.0.0.1:5173",    # 本地IP
        "https://你的生产域名.com"   # 生产环境
    ],
    allow_credentials=True,         # 允许携带cookie
    allow_methods=["*"],            # 允许所有方法 GET、POST等
    allow_headers=["*"],            # 允许所有头
)


@app.get("/items/{message_main}")
async def read_item(message_main:str, q: str = None): # item_id 会自动转换为整数，q 是可选查询参数
    print(message_main)
    async def ask_ollama(message_main: str, model: str = "llama2", host: str = "localhost", port: int = 11434):

#    向本地Ollama模型发送请求
    
   # Args:
   #     prompt: 用户输入的提示词
  #      model: 模型名称，默认为llama2
  #      host: Ollama服务地址，默认为localhost
   #     port: Ollama服务端口，默认为11434
    
   # Returns:
  #      str: 模型生成的响应文本
        url = f"http://{host}:{port}/api/generate"
    
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                return {"item_id": result.get("response", ""), "q": q}
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="无法连接到Ollama服务")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail= "请求超时")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"请求失败: {str(e)}")
    #return {"item_id": message_main, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)