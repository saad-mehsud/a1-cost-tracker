from google import genai
from google.genai import types
from groq import Groq
import dotenv as env
import os
PATH =  os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
ENVPATH = f"{PATH}/.env"

#Load Environment Variables
env.load_dotenv()
GeminiKey = env.get_key(dotenv_path = ENVPATH,key_to_get="GEMINI_API_KEY")
GroqKey = env.get_key(dotenv_path=ENVPATH,key_to_get="GROQ_API_KEY")
geminiClient = genai.Client(api_key=GeminiKey)
groqClient = Groq(api_key=GroqKey)

userMessages = []

def geminiRequest(request):
    interaction = geminiClient.interactions.create(
    model="gemini-4-hydrogen",
    input=request,
    stream=True)
    for events in interaction:
        print(events)
def groqRequest(request):
    global userMessages
    userMessages.append({
        "role":"user",
        "content":request
        
    })
    chat_completion = groqClient.chat.completions.create(
    messages=userMessages,
    model="openai/gpt-oss-120b",
    stream=True
    )
    
    for chunk in chat_completion:
        print(chunk.choices[0].delta.content or "",end="")
    


while(True):
    userInput = input("Enter Your Prompt:")
    if userInput.upper() == "EXIT":
        geminiClient.close()
        groqClient.close()
        break
    groqRequest(userInput)
    print("\n")