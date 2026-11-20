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
def calculateCost(geminiUsage = None,groqUsage = None):
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
        geminiInputCost= (geminiUsage.total_input_tokens/10e6) * GENAI_INPUT_COST
        geminiOutputCost = ((geminiUsage.total_output_tokens + geminiUsage.total_thought_tokens)/10e6)*GENAI_OUTPUT_COST
        geminiCostPerRequest = geminiInputCost + geminiOutputCost
        print(f"Input Cost:{geminiInputCost:.6f}")
        print(f"Output Cost: {geminiOutputCost:.6f}")
        print(f"Total Cost:{geminiCostPerRequest:.6f}")
    #Groq
    if groqUsage is not None:
         
         print("+++++++++++++++++++++")
         print("+++  Groq's Cost  +++")
         print("+++++++++++++++++++++")
         print(f"""Completion Tokens:{groqUsage.completion_tokens}
            \nPrompt Tokens: {groqUsage.prompt_tokens}
            \nTotal Tokens:{groqUsage.total_tokens}""")
         groqInputCost = (groqUsage.prompt_tokens/10e6)*0.15
         groqOutputCost = (groqUsage.completion_tokens/10e6)*0.60
         groqCostPerRequest = groqInputCost+groqOutputCost
         print(f"Input Cost:{groqInputCost:.6f}")
         print(f"Output Cost: {groqOutputCost:.6f}")
         print(f"Total Cost:{groqCostPerRequest:.6f}")
    if geminiUsage is not None and groqUsage is not None:
        print(f"Cost           Gemini           Groq")
        print(f"Input Cost     {geminiInputCost:.6f}           {groqInputCost:.6f}")
        print(f"Output Cost    {geminiOutputCost:.6f}           {groqOutputCost:.6f}")
        print(f"Cost/Req       {geminiCostPerRequest:.6f}           {groqCostPerRequest:.6f}")
        if groqCostPerRequest>geminiCostPerRequest:
            print("Groq Costs More Than Gemini")
        else:
            print("Gemini Costs more than Groq")
    else:
        print("One of the APIs failed to respond comparison table cannot be created.")
                
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