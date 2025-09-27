from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/test-simple")
async def test_simple():
    try:
        async with httpx.AsyncClient() as client:
            # 先测试基础连接
            response = await client.get("http://localhost:11434/api/tags", timeout=5.0)
            return {"status": "success", "ollama_status": response.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)