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
Enter Your Prompt: Explain variables in Python
GEMINI OUTPUT

Variables store references to values, such as numbers or strings.
Groq OUTPUT

A variable is a name that points to a value in a Python program.
+++++++++++++++++++++
+++ Gemini's Cost +++
+++++++++++++++++++++
Initial Input Tokens: 12
Total Output Tokens: 28
Total Input Tokens: 12
Total Thought Tokens: 0
Total Tokens Used: 40
Input Cost:0.000002
Output Cost: 0.000021
Total Cost:0.000023
+++++++++++++++++++++
+++  Groq's Cost  +++
+++++++++++++++++++++
Completion Tokens:20
Prompt Tokens: 18
Total Tokens:38
Input Cost:0.000000
Output Cost: 0.000001
Total Cost:0.000001
Cost           Gemini           Groq
Input Cost     0.000002           0.000000
Output Cost    0.000021           0.000001
Cost/Req       0.000023           0.000001
Gemini Costs more than Groq
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
