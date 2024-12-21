import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Form, File,  UploadFile, HTTPException
from fastapi.responses import JSONResponse
import dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import time


from file_upload import handle_file_upload
from discounts_domestic_air_accesorials import analyze_discounts_domestic_air_accesorials
from discounts_domestic_ground import analyze_discounts_domestic_ground
from discounts_international import analyze_discounts_international
from chat import handle_chat
import asyncio

dotenv.load_dotenv()

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Adjust this to the specific origins you want to allow
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequestBody(BaseModel):
    fileName: str
    weeklyChargesBand: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequestBody(BaseModel):
    fileName: str
    message: str
    chat_history: List[ChatMessage]


def wait_for_file_active(fileName):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.

    This implementation uses a simple blocking polling loop. Production code
    should probably employ a more sophisticated approach.
    """
    print("Waiting for file processing...")

    file = genai.get_file(fileName)
    if not file:
        raise Exception(f"File {fileName} not found")
    while file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(10)
        file = genai.get_file(fileName)
    if file.state.name != "ACTIVE":
        raise Exception(f"File {file.name} failed to process")
    print("...all files ready")

    return file


@app.get("/health")
async def read_root():
    return {"message": "Hello World"}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), weeklyChargesBand: str = Form(...)):
    try:

        if not file or not weeklyChargesBand:
            raise HTTPException(
                status_code=400, detail="File and weeklyChargesBand are required.")

        if file.content_type != 'application/pdf':
            raise HTTPException(
                status_code=400, detail="Only PDF files are accepted.")

        uploadedFile, exactWeeklyBandRange = await handle_file_upload(file, weeklyChargesBand)

        file = wait_for_file_active(uploadedFile.name)

        results = await asyncio.gather(
            analyze_discounts_domestic_air_accesorials(
                file, exactWeeklyBandRange),
            analyze_discounts_domestic_ground(file, exactWeeklyBandRange),
            analyze_discounts_international(file, exactWeeklyBandRange)
        )

        domesticair, accesorials = results[0]
        domesticground1, domesticground2, domesticground3 = results[1]
        international1, international2, response5 = results[2]

        return JSONResponse(status_code=200, content={"file_name": uploadedFile.name,
                                                      "exactWeeklyBandRange": exactWeeklyBandRange,
                                                      "discounts": [
                                                          {
                                                              "domesticAir": domesticair,
                                                              "accesorials": accesorials
                                                          },
                                                          {
                                                              "domesticGround1": domesticground1,
                                                              "domesticGround2":  domesticground2,
                                                              "domesticGround3": domesticground3,
                                                          },
                                                          {
                                                              "international1": international1,
                                                              "international2":  international2,
                                                              "response5": response5,
                                                          }
                                                      ]
                                                      })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(body: ChatRequestBody):
    try:

        if not body.fileName or not body.message:
            return JSONResponse(status_code=400, content={
                "error": "fileName and weeklyChargesBand are required"
            })

        file = wait_for_file_active(body.fileName)

        response = await handle_chat(file, body.message, body.chat_history)

        return JSONResponse(status_code=200, content={"response": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-file")
async def upload_file(file: UploadFile = File(...), weeklyChargesBand: str = Form(...)):
    try:

        if not file or not weeklyChargesBand:
            raise HTTPException(
                status_code=400, detail="File and weeklyChargesBand are required.")

        if file.content_type != 'application/pdf':
            raise HTTPException(
                status_code=400, detail="Only PDF files are accepted.")

        uploadedFile, exactWeeklyBandRange = await handle_file_upload(file, weeklyChargesBand)

        return JSONResponse(status_code=200, content={"file_name": uploadedFile.name, "exactWeeklyBandRange": exactWeeklyBandRange})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/discounts-domestic-air-accesorials")
async def discounts_domestic_air_accesorials(body: AnalysisRequestBody):
    try:

        if not body.fileName or not body.weeklyChargesBand:
            return JSONResponse(status_code=400, content={
                "error": "fileName and weeklyChargesBand are required"
            })

        file = wait_for_file_active(body.fileName)

        domesticair, accesorials = await analyze_discounts_domestic_air_accesorials(file, body.weeklyChargesBand)

        return JSONResponse(status_code=200, content={
            "domesticAir": domesticair,
            "accesorials": accesorials
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/discounts-domestic-ground")
async def discounts_domestic_ground(body: AnalysisRequestBody):
    try:

        if not body.fileName or not body.weeklyChargesBand:
            return JSONResponse(status_code=400, content={
                "error": "fileName and weeklyChargesBand are required"
            })

        file = wait_for_file_active(body.fileName)

        domesticground1, domesticground2, domesticground3 = await analyze_discounts_domestic_ground(file, body.weeklyChargesBand)

        return JSONResponse(status_code=200, content={
            "domesticGround1": domesticground1,
            "domesticGround2":  domesticground2,
            "domesticGround3": domesticground3,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/discounts_international")
async def discounts_international(body: AnalysisRequestBody):
    try:

        if not body.fileName or not body.weeklyChargesBand:
            return JSONResponse(status_code=400, content={
                "error": "fileName and weeklyChargesBand are required"
            })

        file = wait_for_file_active(body.fileName)

        international1, international2, response5 = await analyze_discounts_international(file, body.weeklyChargesBand)

        return JSONResponse(status_code=200, content={
            "international1": international1,
            "international2":  international2,
            "response5": response5,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
