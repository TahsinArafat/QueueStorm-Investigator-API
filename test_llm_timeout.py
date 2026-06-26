import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
model_name = os.environ.get("MODEL_NAME", "gpt-4o-mini")

print(f"Testing direct LLM call...")
print(f"Model: {model_name}")
print(f"Base URL: {base_url[:50]}...")

client = OpenAI(api_key=api_key, base_url=base_url)

start = time.time()
try:
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Reply in JSON."},
            {"role": "user", "content": "Say hello in JSON format with a 'message' field."}
        ],
        response_format={"type": "json_object"},
        timeout=10.0
    )
    elapsed = time.time() - start
    print(f"✅ LLM responded in {elapsed:.2f} seconds")
    print(f"Response: {response.choices[0].message.content[:100]}")
    
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ LLM error after {elapsed:.2f} seconds: {type(e).__name__}: {e}")

