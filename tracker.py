# Imports used in the code
import os,groq,sys,time
from google import genai
from google.genai import types,errors
from groq import Groq
import dotenv as env

#Global variable Declaration
PATH =  os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
ENVPATH = f"{PATH}/.env"
# System instruction that will be passed to both the systems
systemInstruction = """1.Avoid Using Markdown text format in the responses it should be plain text.
2.Do not use Emojis keep the text formal.
3.Your response should contain Maximum 20 words."""

#List for gemini interaction objects to keep the interaction statefull
geminiInteraction = []

#Initialize a groq userMessage List with system prompts
chat_history = [{
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
# These Constants or only for gemini-3.5-flash-lite kindly while testing the code use the same model to
# avoid conflicting output prices.
GENAI_INPUT_COST = 0.30 #USD
GENAI_OUTPUT_COST = 2.50 #USD
# These prices are only for gpt-oss-120b model kindly use the same model while testing the code to avoid 
#conflicting results
GROQ_INPUT_COST = 0.15 #USD
GROQ_OUTPUT_COST =0.60 #USD




#Function to send requests
def geminiRequest(request):
    try:
        
        start_time = time.perf_counter()
        geminiInteraction.append(geminiClient.interactions.create(
            model = GEMINIMODEL,
            input = request,
            system_instruction= systemInstruction,
            previous_interaction_id = geminiInteraction[-1].id if len(geminiInteraction) > 0 else None,
          ))
        end_time = time.perf_counter()
        gemini_elapsed_time = end_time - start_time
        print("GEMINI OUTPUT")
        print(geminiInteraction[-1].output_text)
        return (geminiInteraction[-1].usage,gemini_elapsed_time)
    except errors.APIError as ae:
        print("Gemini Error!!!!!!!!!!!")
        if ae.code in (400,401,403):
            print("Provide a valid and authenticated API Key for Google AI Studio or Gemini.",file=sys.stderr)
        else:
            print(f"Code:{ae.code} Message:{ae.message}")
            return (None,0)
    except errors.ServerError as se:
        print("Gemini Error!!!!!!!!!!!")
        print(f"Internal server error occured:{se}")
    except Exception as e:
        print("Gemini Error!!!!!!!!!!!")
        print(str(e))
        return (None,0)


    
def groqRequest(request):
    try:
        chat_history.append({
            "role":"user",
            "content":request 
        })
        start_time = time.perf_counter()
        chat_completion = groqClient.chat.completions.create(
        messages=chat_history,
        model=GROQMODEL
        )
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print("Groq OUTPUT")
        print(chat_completion.choices[0].message.content)
        #Adds the reply from the assistant to the chat_history list so it remembers its response and do not respond to the same message again 
        chat_history.append({"role":"assistant","content":chat_completion.choices[0].message.content})
        return (chat_completion.usage,elapsed_time)
    except groq.AuthenticationError as ae:
        print("GROQ Error!!!!!!!!!!!")
        print(f"Error occured while authenticating with server.Provide correct API key for groq client.",file=sys.stderr)
        return (None,0)
    except groq.APIError as ae:
        print("GROQ Error!!!!!!!!!!!")
        print(f"Error occured:{ae.message}")
        return (None,0)




## Function to calculate metrics
         
def calculateCost(geminiUsage = None,groqUsage = None):
    #Gemini
    if geminiUsage is not None:
        print("+++ Gemini's Cost +++")     
        print(f"""Total Input Tokens:{geminiUsage.total_input_tokens}
              Total Output Tokens:{geminiUsage.total_output_tokens}
              Total Thought Tokens:{geminiUsage.total_thought_tokens}
              Total Tokens Used:{geminiUsage.total_tokens}""")
        geminiInputCost= (geminiUsage.total_input_tokens/10e6) * GENAI_INPUT_COST
        geminiOutputCost = ((geminiUsage.total_output_tokens + geminiUsage.total_thought_tokens)/10e6)*GENAI_OUTPUT_COST
        geminiCostPerRequest = geminiInputCost + geminiOutputCost
        print(f"Input Cost:{geminiInputCost:.6f}")
        print(f"Output Cost: {geminiOutputCost:.6f}")
        print(f"Total Cost:{geminiCostPerRequest:.6f}")
    #Groq
    if groqUsage is not None:
         print("+++  Groq's Cost  +++")
         print(f"""Completion Tokens:{groqUsage.completion_tokens}
            \nPrompt Tokens: {groqUsage.prompt_tokens}
            \nTotal Tokens:{groqUsage.total_tokens}""")
         groqInputCost = (groqUsage.prompt_tokens/10e6)*GROQ_INPUT_COST
         groqOutputCost = (groqUsage.completion_tokens/10e6)*GROQ_OUTPUT_COST
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



def compareSpeed(geminiTime = 0,groqTime = 0):
    print(f"Gemini Time:{geminiTime:.3f}s" if geminiTime != 0 else "Failed to respond")
    print(f"Groq Time:{groqTime:.3f}s" if groqTime != 0 else "Failed to respond")      
    if geminiTime == 0 or groqTime == 0: 
        print("One or more model/s failed to provide response,comparison cannot be done.")
    elif geminiTime > groqTime:
        print("Groq is faster than Gemini.")
    else:
        print("Gemini is faster than Groq.")         


while(True):
    userInput = input("Enter Your Prompt:")
    if userInput.upper() == "EXIT":
        geminiClient.close()
        groqClient.close()
        break
    groqTokensUsed,groqElapsedTime = groqRequest(userInput)
    geminiTokensUsed,geminiElapsedTime = geminiRequest(userInput)
    calculateCost(geminiTokensUsed,groqTokensUsed)
    compareSpeed(geminiElapsedTime,groqElapsedTime)
    print("\n")