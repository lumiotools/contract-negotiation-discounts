import os
import google.generativeai as genai
from fastapi import FastAPI, File,  UploadFile, HTTPException
from fastapi.responses import JSONResponse
import dotenv
from fastapi import Form
import json

dotenv.load_dotenv()

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

app = FastAPI()


model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/upload-file")
async def upload_to_gemini(file: UploadFile = File(...), weeklyChargesBand: str = Form(...)):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    
    if not file or not weeklyChargesBand:
        raise HTTPException(
            status_code=400, detail="File and weeklyChargesBand are required.")

    if file.content_type != 'application/pdf':
        raise HTTPException(
            status_code=400, detail="Only PDF files are accepted.")

    with open(file.filename, "wb") as f:
        f.write(await file.read())
        
    
    genai.configure(api_key=os.getenv["API_KEY"])

    uploadedFile = genai.upload_file(file.filename, mime_type=file.content_type)
    
    genai.configure(api_key=os.getenv["ALTERNATE_API_KEY"])
    
    uploadedFile = genai.upload_file(file.filename, mime_type=file.content_type)
    
    uploadedFile = genai.get_file("files/7xfmf0p8cpln")
    chat_session = model.start_chat(history=[
        {
            "role": "user",
            "parts": [
                uploadedFile,
                """Use the attached contract to find the table. If there are multiple tables, use the first table. 

                Requirements:
                1. Analyze the weekly charges band ranges in the table
                2. The first range has the minimum value as 0
                3. Find the range where *16,856* falls
                4. Match criteria: min value <= *16,856* <= max value
                5. If no exact range is found, return the highest possible range

                Output Format:
                {{
                    "weeklyChargesBand": "EXACT_RANGE_FOUND"
                }}
                """,
            ],
        },
        {
            "role":"model",
            "parts":[
                "```json\n{\n  \"weeklyChargesBand\": \"0.01 - 19,429.99\"\n}\n```"
            ]
        }
    ])

    response = chat_session.send_message(
        f"""Use the attached contract to find the table. If there are multiple tables, use the first table. 

        Requirements:
        1. Analyze the weekly charges band ranges in the table
        2. The first range has the minimum value as 0
        3. Find the range where *{weeklyChargesBand}* falls
        4. Match criteria: min value <= *{weeklyChargesBand}* <= max value
        5. If no exact range is found, return the highest possible rang
        Output Format:
        {{
            "weeklyChargesBand": "EXACT_RANGE_FOUND"
        }}
        """
    )
    
    exactWeeklyBandRange =json.loads(response.text.replace("```json\n", "").replace("\n```", "") )["weeklyChargesBand"]


    return JSONResponse(status_code=200, content={"file_name": uploadedFile.name,"exactWeeklyBandRange": exactWeeklyBandRange})
