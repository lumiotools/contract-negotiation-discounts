import os
import time
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import dotenv
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file


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


# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel("gemini-1.5-flash")
modelpro = genai.GenerativeModel("gemini-1.5-pro")

class RequestBody(BaseModel):
  fileName: str
  weeklyChargesBand: str
  
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/discounts-domestic-air-accesorials/analyze")
async def analyze(body: RequestBody):
  
  try:
  
    if not body.fileName or not body.weeklyChargesBand:
      return JSONResponse(status_code=400, content={
        "error": "fileName and weeklyChargesBand are required"
      })

    file = wait_for_file_active(body.fileName)

    # chat_sessionpro = modelpro.start_chat(history=[
    #   {
    #       "role":
    #       "user",
    #       "parts": [
    #           file,
    #           f"Use the attached contract to fill the table. the weekly charges band is {body.weeklyChargesBand}. DOMESTIC AIR SERVICE LEVEL WEIGHT RANGE CURRENT UPS\nNext Day Air Letter All\nNext Day Air Package All\nNext Day Air Saver Letter All\nNext Day Air Saver Package All\n2nd Day AM Letter All\n2nd Day AM Package All\n2nd Day Air Letter All\n2nd Day Air Package All\n3 Day Select Package All\nNext Day Air CWT All\nNext Day Air Saver CWT All\n2nd Day Air AM CWT All\n2nd Day Air CWT All\n3 Day Select CWT All",
    #       ],
    #   },
    #   {
    #       "role":
    #       "model",
    #       "parts": [
    #           "```json\n{\"Domestic Air Service Level\": {\"Next Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"Next Day Air Saver\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"2nd Day AM\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"2nd Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"3 Day Select\": {\"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"51.00%\"}}, \"Next Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"Next Day Air Saver CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day AM CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"3 Day Select CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}}}\n```",
    #       ],
    #   },
    # ])

    chat_session = model.start_chat(history=[
      {
          "role":
          "user",
          "parts": [
              file,
              f"Use the attached contract to fill the table. the weekly charges band is {body.weeklyChargesBand}. DOMESTIC AIR SERVICE LEVEL WEIGHT RANGE CURRENT UPS\nNext Day Air Letter All\nNext Day Air Package All\nNext Day Air Saver Letter All\nNext Day Air Saver Package All\n2nd Day AM Letter All\n2nd Day AM Package All\n2nd Day Air Letter All\n2nd Day Air Package All\n3 Day Select Package All\nNext Day Air CWT All\nNext Day Air Saver CWT All\n2nd Day Air AM CWT All\n2nd Day Air CWT All\n3 Day Select CWT All",
          ],
      },
      {
          "role":
          "model",
          "parts": [
              "```json\n{\"Domestic Air Service Level\": {\"Next Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"Next Day Air Saver\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"2nd Day AM\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"2nd Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"3 Day Select\": {\"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"51.00%\"}}, \"Next Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"Next Day Air Saver CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day AM CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"3 Day Select CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}}}\n```",
          ],
      },
    ])


    domesticair = chat_session.send_message(
      '''Use the attached contract to fill the table. return in a json format and only the json of the table and nothing else. the weekly charges band is {body.weeklyChargesBand}. 
      {
        "Domestic Air Service Level": {
          "Next Day Air": {
            "Letter": {
              "Weight Range": "All",
              "Current UPS": ""
            },
            "Package": {
              "Weight Range": "All",
              "Current UPS": ""
            }
          },
          "Next Day Air Saver": {
            "Letter": {
              "Weight Range": "All",
              "Current UPS": ""
            },
            "Package": {
              "Weight Range": "All",
              "Current UPS": ""
            }
          },
          "2nd Day AM": {
            "Letter": {
              "Weight Range": "All",
              "Current UPS": ""
            },
            "Package": {
              "Weight Range": "All",
              "Current UPS": ""
            }
          },
          "2nd Day Air": {
            "Letter": {
              "Weight Range": "All",
              "Current UPS": ""
            },
            "Package": {
              "Weight Range": "All",
              "Current UPS": ""
            }
          },
          "3 Day Select": {
            "Package": {
              "Weight Range": "All",
              "Current UPS": ""
            }
          },
          "Next Day Air CWT": {
            "Weight Range": "All",
            "Current UPS": ""
          },
          "Next Day Air Saver CWT": {
            "Weight Range": "All",
            "Current UPS": ""
          },
          "2nd Day AM CWT": {
            "Weight Range": "All",
            "Current UPS": ""
          },
          "2nd Day Air CWT": {
            "Weight Range": "All",
            "Current UPS": ""
          },
          "3 Day Select CWT": {
            "Weight Range": "All",
            "Current UPS": ""
          }
        }
      }

      ''')  # Note closing parentheses adjusted."

    accesorials = chat_session.send_message(
        '''Use the attached contract to fill the current UPS. All the accesorials and incentives are listed in the attached contract. return in a json format and only the json of the table and nothing else. if current_ups not found for a particular accesorial charge return null
    [
      {
        "ACCESSORIAL_CHARGE": "DAS Comm",
        "TERM": "Air",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Ext Comm",
        "TERM": "Air",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Resi",
        "TERM": "Air",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Ext Resi",
        "TERM": "Air",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Comm",
        "TERM": "Ground",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Ext Comm",
        "TERM": "Ground",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Resi",
        "TERM": "Ground",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "DAS Ext Resi",
        "TERM": "Ground",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "Residential Fee",
        "TERM": "Air",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "Residential Fee",
        "TERM": "Ground",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "Additional Handling - ALL",
        "TERM": "Domestic",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "Additional Handling - ALL",
        "TERM": "Export",
        "CURRENT_UPS": ""
      },
      {
        "ACCESSORIAL_CHARGE": "Duty and Tax Forwarding",
        "TERM": "Export",
        "CURRENT_UPS": ""
      }
    ]
    ''')  # Note closing parentheses adjusted."




    return JSONResponse(status_code=200, content={
      "domesticAir": json.loads(domesticair.text.replace("```json\n", "").replace("\n```", "")),
      "accesorials": json.loads(accesorials.text.replace("```json\n", "").replace("\n```", "")) 
    })

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))