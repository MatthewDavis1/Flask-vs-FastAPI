#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

# Define various message types
class StringOnly(BaseModel):
    message: str

class IntString(BaseModel):
    id: int
    message: str

class Mixed(BaseModel):
    id: int
    value: float
    message: str
    flags: List[bool]

# GET endpoint
@app.get("/get")
def get_endpoint():
    return {"message": "This is a GET response"}

# POST endpoint for StringOnly
@app.post("/post/string")
def post_string(data: StringOnly):
    return {"received": data}

# POST endpoint for IntString
@app.post("/post/int_string")
def post_int_string(data: IntString):
    return {"received": data}

# POST endpoint for Mixed
@app.post("/post/mixed")
def post_mixed(data: Mixed):
    return {"received": data}

# PUT endpoint for StringOnly
@app.put("/put/string")
def put_string(data: StringOnly):
    return {"updated": data}

# PUT endpoint for IntString
@app.put("/put/int_string")
def put_int_string(data: IntString):
    return {"updated": data}

# PUT endpoint for Mixed
@app.put("/put/mixed")
def put_mixed(data: Mixed):
    return {"updated": data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
