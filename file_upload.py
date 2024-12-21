import os
import google.generativeai as genai
import dotenv
import json

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


async def handle_file_upload(file, weeklyChargesBand):

    with open(file.filename, "wb") as f:
        f.write(await file.read())

    uploadedFile = genai.upload_file(
        file.filename, mime_type=file.content_type)

    os.remove(file.filename)

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
            "role": "model",
            "parts": [
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

    exactWeeklyBandRange = json.loads(response.text.replace(
        "```json\n", "").replace("\n```", ""))["weeklyChargesBand"]

    return uploadedFile, exactWeeklyBandRange
