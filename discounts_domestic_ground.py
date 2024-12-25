import os
import google.generativeai as genai
import dotenv
import json

dotenv.load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel("gemini-1.5-flash")
modelpro = genai.GenerativeModel("gemini-2.0-flash-exp")


async def analyze_discounts_domestic_ground(file, weeklyChargesBand):

    chat_sessionpro = modelpro.start_chat(history=[
        {
            "role":
            "user",
            "parts": [
                file,
                f"Use the attached contract to fill the table. the weekly charges band is {weeklyChargesBand}. DOMESTIC AIR SERVICE LEVEL WEIGHT RANGE CURRENT UPS\nNext Day Air Letter All\nNext Day Air Package All\nNext Day Air Saver Letter All\nNext Day Air Saver Package All\n2nd Day AM Letter All\n2nd Day AM Package All\n2nd Day Air Letter All\n2nd Day Air Package All\n3 Day Select Package All\nNext Day Air CWT All\nNext Day Air Saver CWT All\n2nd Day Air AM CWT All\n2nd Day Air CWT All\n3 Day Select CWT All",
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
    chat_session = model.start_chat(history=[
        {
            "role":
            "user",
            "parts": [
                file,
                f"Use the attached contract to fill the table. the weekly charges band is {weeklyChargesBand}. DOMESTIC AIR SERVICE LEVEL WEIGHT RANGE CURRENT UPS\nNext Day Air Letter All\nNext Day Air Package All\nNext Day Air Saver Letter All\nNext Day Air Saver Package All\n2nd Day AM Letter All\n2nd Day AM Package All\n2nd Day Air Letter All\n2nd Day Air Package All\n3 Day Select Package All\nNext Day Air CWT All\nNext Day Air Saver CWT All\n2nd Day Air AM CWT All\n2nd Day Air CWT All\n3 Day Select CWT All",
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

    domesticground1 = chat_sessionpro.send_message('''
            Use the attached contract to populate the table. Focus only on the weekly charge bands ($) range of {weeklyChargesBand} from the portfolio tier incentive table. only get the values from the portfolio tier incentive table for the correct weekly charge bands. Return the result in JSON format, containing only the table data and nothing else.

            {
              "DOMESTIC GROUND SERVICE LEVEL": {
                "UPS® Ground - Commercial Package - Prepaid": {
                  "Weight Range": "All",
                  "Current UPS": ""
                },
                "UPS® Ground - Residential Package - Prepaid": {
                  "Weight Range": "All",
                  "Current UPS": ""
                }
              }
            }
            ''')

    domesticground2 = chat_sessionpro.send_message('''
            Use the attached contract to populate the table. Focus only on the weekly charge bands ($) range of 37,780.00 - 43,174.99 from the portfolio tier incentive table. Return the result in JSON format, containing only the table data and nothing else.

        {
          "DOMESTIC GROUND SERVICE LEVEL": {
            "UPS® Ground - Commercial Package - Prepaid - Incentives Off Effective Rates": {
              "1-5 lbs": "",
              "6-10 lbs": "",
              "11-20 lbs": "",
              "21-30 lbs": "",
              "31-50 lbs": "",
              "51-70 lbs": "",
              "71-150 lbs": "",
              "151 lbs+": ""
            },
            "UPS® Ground - Residential Package - Prepaid - Incentives Off Effective Rates": {
              "1-5 lbs": "",
              "6-10 lbs": "",
              "11-20 lbs": "",
              "21-30 lbs": "",
              "31-50 lbs": "",
              "51-70 lbs": "",
              "71-150 lbs": "",
              "151 lbs+": ""
            }
          }
        }


            ''')

    domesticground3 = chat_session.send_message(
        '''Use the attached contract to fill the table. return in a json format and only the json of the table and nothing else. there should be 2 rows. commodity tier is in addendum 1. the weekly charges band is 37,780.00 - 43,174.99. 

           {
             "DOMESTIC GROUND SERVICE LEVEL": {
               "Ground CWT": {
                 "Weight Range": "All",
                 "Current UPS": "",
                 "Discount": "",
                 "Tier": ""
               }
             }
           }

        ''')

    domesticground1 = json.loads(domesticground1.text.replace(
        '```json\n', '').replace('\n```', ''))
    domesticground2 = json.loads(domesticground2.text.replace(
        '```json\n', '').replace('\n```', ''))
    domesticground3 = json.loads(domesticground3.text.replace(
        '```json\n', '').replace('\n```', ''))

    return domesticground1, domesticground2, domesticground3
