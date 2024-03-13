from fastapi import FastAPI, HTTPException
import httpx
import re

app = FastAPI()

def validar_cep(cep: str) -> bool:
    return re.fullmatch(r"\d{5}-?\d{3}", cep) is not None

async def consultar_cep_externo(cep: str) -> dict:
    url = f"https://viacep.com.br/ws/{cep}/json/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=404, detail="CEP não encontrado")

def salvar_cache(cache: dict):
    with open("cep_cache.txt", "w") as file:
        for cep, dados in cache.items():
            file.write(f"{cep}:{dados}\n")

def carregar_cache() -> dict:
    cache = {}
    try:
        with open("cep_cache.txt", "r") as file:
            for line in file:
                cep, dados = line.strip().split(":")
                cache[cep] = dados
    except FileNotFoundError:
        pass
    return cache

cep_cache = carregar_cache()

@app.get("/cep/{cep}")
async def buscar_cep(cep: str):
    cep = cep.replace("-", "")
    
    if not validar_cep(cep):
        raise HTTPException(status_code=400, detail="Formato de CEP inválido")
    
    if cep in cep_cache:
        return {"data": cep_cache[cep], "cache": True}
    
    dados_cep = await consultar_cep_externo(cep)
    if cep not in cep_cache:  
        cep_cache[cep] = dados_cep
        salvar_cache(cep_cache)
    
    return {"data": dados_cep, "cache": False}

@app.get("/cache/{cep}")
async def consultar_cache(cep: str):
    cep = cep.replace("-", "")
    
    if cep in cep_cache:
        return {"data": cep_cache[cep]}
    else:
        raise HTTPException(status_code=404, detail="CEP não encontrado no cache")

@app.get("/cache")
async def consultar_todo_cache():
    return {"data": cep_cache}
