# IEC Assignment 1: AI Cost Tracker

This project compares responses and estimated token costs from Google Gemini and
Groq. It sends the same prompt to both providers, displays both responses, and
prints token usage, estimated input/output costs, and a comparison.

## Requirements

- Python 3.14 or newer
- API keys for [Google AI Studio](https://aistudio.google.com/api-keys) and
  [Groq](https://console.groq.com/keys)
- `uv` (recommended) or another Python package manager

## Setup and Usage

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file by copying `.env.example`:

   ```bash
   cp .env.example .env
   ```

3. Replace the placeholder values in `.env` with your API keys and the model
   names you want to use:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODELS=your_gemini_model
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=your_groq_model
   ```

   Do not commit `.env` or share your API keys.

4. Start the tracker:

   ```bash
   uv run tracker.py
   ```

5. Enter a prompt when asked. Type `EXIT` to close the clients and stop the
   program.

## Sample Output

The model responses and token counts vary for every request. A typical run
looks like this:

```text
Enter Your Prompt:what is AI 
Groq OUTPUT
Artificial intelligence is the field of computer science that creates systems capable of learning, reasoning, and decision‑making.
GEMINI OUTPUT
Artificial Intelligence is the simulation of human intelligence by computer systems, enabling machines to learn, reason, and solve problems.
+++ Gemini's Cost +++
Total Input Tokens:49
              Total Output Tokens:23
              Total Thought Tokens:0
              Total Tokens Used:72
Input Cost:0.000001
Output Cost: 0.000006
Total Cost:0.000007
+++  Groq's Cost  +++
Completion Tokens:167
            
Prompt Tokens: 116
            
Total Tokens:283
Input Cost:0.000002
Output Cost: 0.000010
Total Cost:0.000012
Cost           Gemini           Groq
Input Cost     0.000001           0.000002
Output Cost    0.000006           0.000010
Cost/Req       0.000007           0.000012
Groq Costs More Than Gemini
Gemini Time:7.777s
Groq Time:1.614s
Groq is faster than Gemini.


Enter Your Prompt:Who was the first person to discover the land of America
Groq OUTPUT
The first known European to reach America was Christopher Columbus in 1492.
GEMINI OUTPUT
Indigenous peoples were the first to inhabit America, while Christopher Columbus led the first documented European voyage there.
+++ Gemini's Cost +++
Total Input Tokens:85
              Total Output Tokens:20
              Total Thought Tokens:0
              Total Tokens Used:105
Input Cost:0.000003
Output Cost: 0.000005
Total Cost:0.000008
+++  Groq's Cost  +++
Completion Tokens:179
            
Prompt Tokens: 159
            
Total Tokens:338
Input Cost:0.000002
Output Cost: 0.000011
Total Cost:0.000013
Cost           Gemini           Groq
Input Cost     0.000003           0.000002
Output Cost    0.000005           0.000011
Cost/Req       0.000008           0.000013
Groq Costs More Than Gemini
Gemini Time:3.086s
Groq Time:1.527s
Groq is faster than Gemini.


Enter Your Prompt:What is the difference between science and philosophy 
Groq OUTPUT
Science empirically tests hypotheses about the natural world; philosophy critically examines concepts, reasoning, and fundamental questions beyond empirical verification.
GEMINI OUTPUT
Science relies on empirical observation and experimentation, whereas philosophy uses rational argument and conceptual analysis to understand existence.
+++ Gemini's Cost +++
Total Input Tokens:116
              Total Output Tokens:20
              Total Thought Tokens:0
              Total Tokens Used:136
Input Cost:0.000003
Output Cost: 0.000005
Total Cost:0.000008
+++  Groq's Cost  +++
Completion Tokens:186
            
Prompt Tokens: 193
            
Total Tokens:379
Input Cost:0.000003
Output Cost: 0.000011
Total Cost:0.000014
Cost           Gemini           Groq
Input Cost     0.000003           0.000003
Output Cost    0.000005           0.000011
Cost/Req       0.000008           0.000014
Groq Costs More Than Gemini
Gemini Time:3.590s
Groq Time:1.810s
Groq is faster than Gemini.


Enter Your Prompt:Now Why was british empire called a Colonial System
Groq OUTPUT
Because Britain established overseas settlements, exploited resources, governed territories, and imposed political control over colonized peoples.
GEMINI OUTPUT
It was called a colonial system because Britain established control over vast overseas territories to extract economic resources.
+++ Gemini's Cost +++
Total Input Tokens:147
              Total Output Tokens:19
              Total Thought Tokens:0
              Total Tokens Used:166
Input Cost:0.000004
Output Cost: 0.000005
Total Cost:0.000009
+++  Groq's Cost  +++
Completion Tokens:188
            
Prompt Tokens: 236
            
Total Tokens:424
Input Cost:0.000004
Output Cost: 0.000011
Total Cost:0.000015
Cost           Gemini           Groq
Input Cost     0.000004           0.000004
Output Cost    0.000005           0.000011
Cost/Req       0.000009           0.000015
Groq Costs More Than Gemini
Gemini Time:6.639s
Groq Time:1.401s
Groq is faster than Gemini.


Enter Your Prompt:Did british introduced this system are was someone else
Groq OUTPUT
Britain expanded earlier European colonial models; Spain and Portugal pioneered colonization, Britain later adopted and systematized it.
GEMINI OUTPUT
Britain did not invent colonialism, as many ancient and contemporary powers also established vast global empires.
+++ Gemini's Cost +++
Total Input Tokens:177
              Total Output Tokens:18
              Total Thought Tokens:0
              Total Tokens Used:195
Input Cost:0.000005
Output Cost: 0.000005
Total Cost:0.000010
+++  Groq's Cost  +++
Completion Tokens:188
            
Prompt Tokens: 276
            
Total Tokens:464
Input Cost:0.000004
Output Cost: 0.000011
Total Cost:0.000015
Cost           Gemini           Groq
Input Cost     0.000005           0.000004
Output Cost    0.000005           0.000011
Cost/Req       0.000010           0.000015
Groq Costs More Than Gemini
Gemini Time:7.082s
Groq Time:1.881s
Groq is faster than Gemini.


Enter Your Prompt:exit

```

The exact formatting and values depend on the selected models and the API
responses.

## What I Learned

I started with the basics and built the project step by step. Through the
repository history, I learned how to:

- create a Python project and manage dependencies with `uv`;
- organize code with imports, variables, constants, and functions;
- load configuration and secrets from environment variables with `python-dotenv`;
- create and use Gemini and Groq API clients;
- send requests and read model responses and token-usage metadata;
- maintain conversation state using Python lists and previous interaction IDs;
- handle authentication and API errors with exceptions;
- calculate input, output, and total costs from token counts;
- compare the cost of two providers in a readable table; and
- improve code clarity through incremental refactoring, reusable constants,
  better output formatting, and clearer error handling.

The commit history reflects this progression: it begins with a basic Python
program, adds Gemini integration, then Groq integration and conversation
handling, and finally adds usage tracking, cost calculations, comparisons, and
pricing constants.
