# Imports used in the code
from google import genai
from google.genai import types
from groq import Groq,GroqError
import dotenv as env
import os

#Global variable Declaration
PATH =  os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
ENVPATH = f"{PATH}/.env"
# System instruction that will be passed to both the systems
systemInstruction = "1.Avoid Using Markdown text format 2.Do not use Emojis keep the text forma"

#List for gemini interaction objects to keep the interaction statefull
geminiInteraction = []

#Initialize a groq userMessage List with system prompts
userMessages = [{
    "role":"system",
    "content":systemInstruction
    }]

#Load Environment Variables
env.load_dotenv()
GEMINIKEY = env.get_key(dotenv_path = ENVPATH,key_to_get="GEMINI_API_KEY")
GROQKEY = env.get_key(dotenv_path=ENVPATH,key_to_get="GROQ_API_KEY")
GROQMODEL = env.get_key(dotenv_path=ENVPATH,key_to_get="GROQ_MODEL")
GEMINIMODEL = env.get_key(dotenv_path=ENVPATH,key_to_get="GEMINI_MODELS")

#Client creation to open a connection to the server
geminiClient = genai.Client(api_key=GEMINIKEY)
groqClient = Groq(api_key=GROQKEY)

#Function to send requests
def geminiRequest(request):
    try:
        geminiInteraction.append(geminiClient.interactions.create(
            model = GEMINIMODEL,
            input = request,
            system_instruction= systemInstruction,
            previous_interaction_id = geminiInteraction[-1].id if len(geminiInteraction) > 0 else None,
          ))
        print(geminiInteraction[-1].output_text)
        return geminiInteraction[-1].usage
    except Exception as e:
        print(f"An error occured:{e}")
def groqRequest(request):
    # global userMessages
    try:
        userMessages.append({
            "role":"user",
            "content":request 
        })
        chat_completion = groqClient.chat.completions.create(
        messages=userMessages,
        model=GROQMODEL
        )
        print(chat_completion.choices[0].message.content)
        return chat_completion.usage
    except GroqError as ge:
         print(f"Error Occured{ge}")
    
    # print(chat_completion.usage)
def calculateCost(geminiUsage,groqUsage):
    print(f"Gemini Usage:{geminiUsage}")
    print(f"Groq Usge:{groqUsage}")
userInput = "Explain How AI Works in 10 words"
print("GEMINI OUTPUT\n")
geminiTokensUsed = geminiRequest(userInput)
print("Groq OUTPUT\n")
groqRequest(userInput)
print(f"\nGroq input lists:{userMessages}")
print("\n")

while(True):
    userInput = input("Enter Your Prompt:")
    if userInput.upper() == "EXIT":
        geminiClient.close()
        groqClient.close()
        break
    print("GEMINI OUTPUT\n")
    geminiTokensUsed = geminiRequest(userInput)
    print("Groq OUTPUT\n")
    groqTokensUsed = groqRequest(userInput)
    calculateCost(geminiTokensUsed,groqTokensUsed)
    print(f"\nGroq input lists:{userMessages}")
    print("\n")