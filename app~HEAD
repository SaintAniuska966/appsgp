from dataclasses import Field
import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Filed, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor asyncio 

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorCliente(os.environ["mongodb+srv://Grupo4C4:<ApDpJpVr4>@cluster0.azxogt6.mongodb.net/?retryWrites=true&w=majority"])
db = client.MisionTic

class PyObjectId(ObjectId):
    @classmethod
    def _get_validators (cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):    
            raise ValueError("Invalid objectiv")
        return ObjectId(v)
    
    @classmethod
    def _modify_schema_(cls,field_schema):
        field_schema.update(type="string")

class StudentModel (BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    Nombre: str = Field(...)
    email: EmailStr = Field(...)
    Curso: str = Field(...)
    Edad: int = Field(..., le = 40)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
            "Nombre": "Jane Doe",
            "email": "jdoe@example.com",
            "Curso": "Desarrollo de Aplicaciones Web",
            "Edad": 23
            }
        } 

class UpdateStudentModel(BaseModel):
    Nombre : Optional[str]
    email : Optional[EmailStr]
    Curso : Optional[str]
    Edad : Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
            "Nombre": "Jane Doe",
            "email": "jdoe@example.com",
            "Curso": "Desarrollo de Aplicaciones Web",
            "Edad": 30
            }
        } 

    @app.post("/", response_description="Add new student", response_model=StudentModel)
    async def create_student(student: StudentModel = Body(...)):
        student = jsonable_encoder(student)
        new_student = await db["Tripulantes"].insert_one(student)
        created_student = await db["Tripulantes"].find_one({"id":new_student.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

    @app.get("/", response_description="List all students", response_model=StudentModel)        
    async def list_students():
        students = await db["Tripulantes"].find().to_list(1000)
        return students

@app.get("/{id}", response_description="Get a single student", response_model=StudentModel)
async def show_student(id: str):
    if (student:= await db["Tripulantes"].find_one({"id": id})) is not None:
        return student
    raise HTTPException(status code=404, detail=f"student {id} not found")

@app.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await db["Tripulantes"].update_one({"id": id}, {"$set": student})
        if update_result.modified_count == 1:
            if ( update_student := await db["Tripulantes"].find_one({"id": id})) is not None:
                return update_student
            
                if (existing_student := await db["Tripulantes"].find_one({"id": id})) is not None:
                    return existing_student
                
    raise HTTPException(status_code=404, detail=f"Student {id} not found")
            
@app.delete("/"{id}, response_description="Delete a student")
async def delete_student(id:str):
    delete_result = await db["Tripulantes"].delete_one({"_id": id})

    if delete_result.delete_count == 1:
        return Response(status code = status.HTTP 204 NO CONTENT)
        
    raise HTTPException(status code=404, detail=f"Student {id} not found")

                    




    

        
