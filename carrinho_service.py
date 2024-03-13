from fastapi import FastAPI

app = FastAPI()

cart = {}

@app.post("/carrrinho/{user_id}/add")
async def add_carrinho(user_id: int, produto_id: int, quantidade: int):
    cart[user_id] = {"produto_id": produto_id, "quantidade": quantidade}
    return {"status": "sucesso", "mensagem": "Produto adicionado ao carrinho"}
