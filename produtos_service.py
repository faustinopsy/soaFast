from fastapi import FastAPI

app = FastAPI()

@app.get("/produtos")
async def listar_produtos():
    return {"produtos": [{"id": 1, "nome": "Produto A", "preco": 100},
                         {"id": 2, "nome": "Produto B", "preco": 150}]}
