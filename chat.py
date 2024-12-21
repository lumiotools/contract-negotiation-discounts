import os
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_chat(file, message, chat_history):
    history = [
        {
            "role": "user",
            "parts": [
                    file,
                    "Use the attached contract as a context to answer my queries"
            ]
        }
    ]

    for chat in chat_history:
        history.append({
            "role": chat.role,
            "parts": [
                chat.content
            ]
        })

    chat_session = model.start_chat(history=history)

    response = chat_session.send_message(message)

    return response.text
