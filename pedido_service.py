from fastapi import FastAPI

app = FastAPI()

@app.post("/pedido/{user_id}/add")
async def criar_pedido(user_id: int):
   return {"status": "sucesso", "mensagem": "Pedido criado", "order_id": 123}
