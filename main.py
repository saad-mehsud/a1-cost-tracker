from google import genai
from google.genai import types
import dotenv as env
import os
print(genai.__version__)
PATH =  os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
ENVPATH = f"{PATH}/.env"

#Load Environment Variables
env.load_dotenv()
GeminiKey = env.get_key(dotenv_path = ENVPATH,key_to_get="GEMINI_API_KEY")




