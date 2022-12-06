from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from uuid import uuid4 as uuid
from datetime import datetime
import uvicorn

app = FastAPI()

paquetes=[]

class Paquete(BaseModel):
    NombreRemmitente:str
    NombreReceptor:str
    FechadeEnvio:datetime =datetime.now()
    TipoPaquete:str

@app.get("/")
def root():
    return {"HOLA!!": "BIENVENIDOS A FASTAPI CON CRUD"}

@app.get("/paquetes")
def get_paquetes():
    return paquetes

@app.post("/paquetes")
def save_paquete(paquetes:Paquete):
    paquetes.id =str(uuid())
    paquetes.append(paquetes.dict())    
    return paquetes[-1]

@app.get("paquetes/{paquetes_id}")
def get_paquete(paquetes_id:str):
    for post in paquetes:
        if paquetes["id"]== paquetes_id:
            return post
        
@app.delete("/paquetes/{paquetes_id}")
def delete_paquete(paquetes_id:str):
    for index, post in enumerate(paquetes):
        if post["id"]== paquetes_id:   
            paquetes.pop(index)
            return{"El paquete ha sido eliminado exitosamente"}
        
@app.put("paquetes/{paquetes_id}")
def upate_paquete(paquetes_id:str, updatePaquete:Paquete):
    for index, post in enumerate(paquetes):
        if paquetes["id"]==paquetes_id:
            paquetes[index]["NombreRemitente"]= updatePaquete.dict()["NombreRemitente"]
            paquetes[index]["NombreReceptor"]= updatePaquete.dict()["NombreReceptor"]
            paquetes[index]["tipoPaquete"]= updatePaquete.dict()["tipoPaquete"]     




    



