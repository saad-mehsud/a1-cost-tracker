# Imports used in the code
from google import genai
from google.genai import types,errors
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

#Constants 
# These Constants or only for gemini-4-hydrogen kindly while testing the code use the same model to
# avoid conflicting output prices.
GENAI_INPUT_COST = 1.5 #USD
GENAI_OUTPUT_COST = 7.50 #USD

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
    except errors.ServerError as se:
        pass
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
         return None
    
    # print(chat_completion.usage)
def calculateCost(geminiUsage = None,groqUsage = None):
    # print(f"Gemini Usage:{geminiUsage}")
    # print(f"Groq Usge:{groqUsage}")
    #Gemini
    if geminiUsage is not None:
        print("+++++++++++++++++++++")
        print("+++ Gemini's Cost +++")
        print("+++++++++++++++++++++")        
        print(f"""Initial Input Tokens{geminiUsage.initial_input_tokens}
              \nTotal Output Tokens:{geminiUsage.total_output_tokens}
              \nTotal Input Tokens:{geminiUsage.total_input_tokens}
              \nTotal Thought Tokens:{geminiUsage.total_thought_tokens}
              \nTotal Tokens Used:{geminiUsage.total_tokens}""")
        inputCost= (geminiUsage.total_input_tokens/10e6) * GENAI_INPUT_COST
        outputCost = ((geminiUsage.total_output_tokens + geminiUsage.total_thought_tokens)/10e6)*GENAI_OUTPUT_COST
        geminiCostPerRequest = inputCost + outputCost
        print(f"Input Cost:{inputCost:.6f}")
        print(f"Output Cost: {outputCost:.6f}")
        print(f"Total Cost:{geminiCostPerRequest:.6f}")
    #Groq
    if groqUsage is not None:
         
         print("+++++++++++++++++++++")
         print("+++  Groq's Cost  +++")
         print("+++++++++++++++++++++")
         print(f"""Completion Tokens:{groqUsage.completion_tokens}
            \nPrompt Tokens: {groqUsage.prompt_tokens}
            \nTotal Tokens:{groqUsage.total_tokens}""")
         inputCost = (groqUsage.prompt_tokens/10e6)*0.15
         outputCost = (groqUsage.completion_tokens/10e6)*0.60
         groqCostPerRequest = inputCost+outputCost
         print(f"Input Cost:{inputCost:.6f}")
         print(f"Output Cost: {outputCost:.6f}")
         print(f"Total Cost:{groqCostPerRequest:.6f}")
    if geminiUsage is not None and groqUsage is not None:
        pass
                
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
    print("\n")