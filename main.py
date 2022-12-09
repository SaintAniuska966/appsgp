import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
#import pymongo

# Clase Paquete
app = FastAPI()
Paquetes = motor.motor_asyncio.AsyncIOMotorClient(os.environ["mongodb+srv://Grupo4C4:<ApDpJpVr4>@cluster0.azxogt6.mongodb.net/?retryWrites=true&w=majority"])
db = Paquetes.Paquete


class PyObjectId(ObjectId):
    @classmethod
    def _get_validators_(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def _modify_schema_(cls, field_schema):
        field_schema.update(type="string")


class PackageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_paquetes: int = Field(..., le=10)
    largo: float = Field(..., le=10)
    ancho: float = Field(..., le=10)
    alto: float = Field(..., le=10)
    peso: float = Field(..., le=10)
    id_tipo: str = Field(..., le=15)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_paquetes": 123456,
                "largo": 25,
                "ancho": 45,
                "alto": 55.6,
                "peso": 10,
                "id_tipo": "Dimensionado"
            }
        }

class UpdatePackageModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    edad: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_paquetes": 6578423,
                "largo": 15,
                "ancho": 25,
                "alto": 30,
                "peso": 5,
                "id_tipo": "Normal"
            }
        }


@app.post("/", response_description="Add new package", response_model=PackageModel)
async def create_paquete(package: PackageModel = Body(...)):
    package = jsonable_encoder(package)
    new_package = await db["Paquetes"].insert_one(package)
    created_package = await db["Paquetes"].find_one({"_id": new_package.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_package)


@app.get(
"/", response_description="List all package", response_model=List[PackageModel]
)
async def list_package():
    package = await db["Paquetes"].find().to_list(1000)
    return package


@app.get(
    "/{id}", response_description="Get a single package", response_model=PackageModel
)
async def show_package(id: str):
    if (package := await db["Paquetes"].find_one({"_id": id})) is not None:
        return package

    raise HTTPException(status_code=404, detail=f"Package {id} not found")


@app.put("/{id}", response_description="Update a package", response_model=PackageModel)
async def update_package(id: str, package: UpdatePackageModel = Body(...)):
    package = {k: v for k, v in package.dict().items() if v is not None}

    if len(package) >= 1:
        update_result = await db["Paquetes"].update_one({"_id": id}, {"$set": package})

        if update_result.modified_count == 1:
            if (
                updated_package := await db["Paquetes"].find_one({"_id": id})
            ) is not None:
                return updated_package

    if (existing_package := await db["Paquetes"].find_one({"_id": id})) is not None:
        return existing_package

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/{id}", response_description="Delete a package")
async def delete_package(id: str):
    delete_result = await db["Paquete"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Package {id} not found")

# Clase Cliente

app = FastAPI()
Paquetes = motor.motor_asyncio.AsyncIOMotorClient(os.environ["mongodb+srv://Grupo4C4:<ApDpJpVr4>@cluster0.azxogt6.mongodb.net/?retryWrites=true&w=majority"])
db = Paquetes.Cliente


class PyObjectId(ObjectId):
    @classmethod
    def _get_validators_(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def _modify_schema_(cls, field_schema):
        field_schema.update(type="string")


class ClientModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Cedula: int = Field(..., le=10)
    Nombre: str = Field(..., le=20)
    Apellido: str = Field(..., le=20)
    Direccion: str = Field(..., le=40)
    Telefono: int = Field(..., le=10)
    Correo: str = Field(..., le=20)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Cedula": 0,
                "Nombre": "",
                "Apellido": "",
                "Direccion": "",
                "Telefono": 10,
                "Correo": ""
            }
        }

class UpdateClientModel(BaseModel):
    Cedula: Optional(int)
    Nombre: Optional[str]
    Apellido: Optional[str]
    Direccion: Optional[str]
    Telefono: Optional[int]
    Correo: Optional(EmailStr)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "example": {
                "Cedula": 45639214,
                "Nombre": "Juan Sebastian",
                "Apellido": "Alvarez",
                "Direccion": "Calle 127 No.98-23",
                "Telefono": 3156302144,
                "Correo": "jse05@gmail.com"
            }
        }
        }        

@app.post("/", response_description="Add new Client", response_model=ClientModel)
async def create_client(client: ClientModel = Body(...)):
    client = jsonable_encoder(client)
    new_client = await db["Paquetes"].insert_one(client)
    created_client = await db["Paquetes"].find_one({"_id": new_client.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_client)


@app.get(
"/", response_description="List all client", response_model=List[ClientModel]
)
async def list_client():
    client = await db["Paquetes"].find().to_list(1000)
    return client


@app.get("/{id}", response_description="Get a single Client", response_model=ClientModel)
async def show_client(id: str):
    if (client := await db["Paquetes"].find_one({"_id": id})) is not None:
        return client

    raise HTTPException(status_code=404, detail=f"Package {id} not found")


@app.put("/{id}", response_description="Update a client", response_model=ClientModel)
async def update_client(id: str, client: UpdateClientModel = Body(...)):
    client = {k: v for k, v in client.dict().items() if v is not None}

    if len(client) >= 1:
        update_result = await db["Paquetes"].update_one({"_id": id}, {"$set": client})

        if update_result.modified_count == 1:
            if (
                updated_client := await db["Paquetes"].find_one({"_id": id})
            ) is not None:
                return updated_client

    if (existing_client := await db["Paquetes"].find_one({"_id": id})) is not None:
        return existing_client

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/{id}", response_description="Delete a client")
async def delete_client(id: str):
    delete_result = await db["Paquete"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Client {id} not found")

# Clase Facturas

app = FastAPI()
Paquetes = motor.motor_asyncio.AsyncIOMotorClient(os.environ["mongodb+srv://Grupo4C4:<ApDpJpVr4>@cluster0.azxogt6.mongodb.net/?retryWrites=true&w=majority"])
db = Paquetes.Facturas


class PyObjectId(ObjectId):
    @classmethod
    def _get_validators_(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def _modify_schema_(cls, field_schema):
        field_schema.update(type="string")


class FacturaModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_paquetes: int = Field(..., le=10)
    num_guia: int = Field(..., le=6)
    fecha: str = Field(..., le=20)
    cedula_remitente: int = Field(..., le=10)
    direccion_remitente: str = Field(..., le=10)
    telefono_remitente: int = Field(..., 10)
    email_remitente: str = Field(..., le=20)
    cedula_destinatario: int = Field(..., le=10)
    direccion_destinatario: str = Field(..., le=10)
    telefono_destinatario: int = Field(..., 10)
    email_destinatario: str = Field(..., le=20)
    ciudad_origen: str = Field(..., le= 20)
    ciudad_destino: str = Field(..., le=20)
    estado_envio: str = Field(..., le=10)
    valor_factura: int = Field(..., le=10)


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_paquete": 1234568,
                "num_guia": 2532,
                "fecha": "2016-01-01-01T000.00.000Z",
                "cedula_remitente": 1025102430,
                "nombre_remitente": "Fabiola Suarez",
                "direccion_remitente": "Kra. 45 No. 25-50",                
                "telefono_remitente": 3005694781,
                "email_remitente": "fabi89@gmail.com",
                "cedula_destinatario": 1023456879,
                "nombre_destinatario": "Carlos Hernandez",
                "direccion_destinatario": "Calle 25 No. 34-98",            
                "telefono_destinatario": 3202541369,
                "email_destinatario": "Carher90@gmail.com",
                "ciudad_origen": "Bogota",
                "ciudad destino": "Medellin",
                "estado_envio": "Transito",
                "valor_fact": 50000
            }
        }

class UpdateFacturaModel(BaseModel):
    id_paquete: Optional(int)
    num_guia: Optional(int)
    fecha: Optional()
    cedula_remitente: Optional(int)
    nombre_remitente: Optional[str]
    direccion_remitente: Optional[str]
    telefono_remitente: Optional[int]
    email_remitente: Optional[EmailStr]
    cedula_destinatario: Optional(int)
    nombre_destinatario: Optional[str]
    direccion_destinatario: Optional[str]
    telefono_destinatario: Optional[int]
    email_destinatario: Optional[EmailStr]
    

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_paquete": 0,
                "num_guia": 0,
                "fecha": "2016-01-01-01T000.00.000Z",
                "cedula_remitente": 0,
                "nombre_remitente": "",
                "direccion_remitente": "",
                "telefono_remitente": 0,
                "email_remitente": "",
                "cedula_destinatario": 0,
                "nombre_destinatario": "",
                "direccion_destinatario": "",
                "telefono_destinatario": 0,
                "email_destinatario": "",
                "ciudad_origen": "",
                "ciudad destino": "",
                "estado_envio": "",
                "valor_fact": 0
            }
        }

@app.post("/", response_description="Add new Factura", response_model=FacturaModel)
async def create_factura(factura: FacturaModel = Body(...)):
    Factura = jsonable_encoder(factura)
    new_Factura = await db["Paquetes"].insert_one(factura)
    created_factura = await db["Paquetes"].find_one({"_id": new_Factura.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_factura)


@app.get(
"/", response_description="List all factura", response_model=List[FacturaModel]
)
async def list_factura():
    factura = await db["Paquetes"].find().to_list(1000)
    return factura


@app.get("/{id}", response_description="Get a single Factura", response_model=FacturaModel)
async def show_factura(id: str):
    if (factura := await db["Paquetes"].find_one({"_id": id})) is not None:
        return factura

    raise HTTPException(status_code=404, detail=f"Package {id} not found")


@app.put("/{id}", response_description="Update a factura", response_model=FacturaModel)
async def update_facturas(id: str, factura: UpdateFacturaModel = Body(...)):
    factura = {k: v for k, v in factura.dict().items() if v is not None}

    if len(factura) >= 1:
        update_result = await db["Paquetes"].update_one({"_id": id}, {"$set": factura})

        if update_result.modified_count == 1:
            if (
                updated_factura := await db["Paquetes"].find_one({"_id": id})
            ) is not None:
                return updated_factura

    if (existing_factura := await db["Paquetes"].find_one({"_id": id})) is not None:
        return existing_factura
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/{id}", response_description="Delete a factura")
async def delete_factura(id: str):
    delete_result = await db["Paquete"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Factura {id} not found")