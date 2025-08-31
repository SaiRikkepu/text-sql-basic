from langchain_openai import ChatOpenAI
from openai import OpenAI
import os

# Load .env first
from dotenv import load_dotenv
load_dotenv()

# ---------- Automatic Model Fallback ----------
# List of preferred models in order
preferred_models = ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
selected_model = None

for model_name in preferred_models:
    try:
        # Try a small test completion
        client.chat.completions.create(
            model=model_name,
            messages=[{"role":"user","content":"Hello"}],
            max_tokens=5
        )
        selected_model = model_name
        print(f"✅ Using model: {selected_model}")
        break
    except Exception as e:
        print(f"⚠️ Model {model_name} not available: {e}")

if selected_model is None:
    raise RuntimeError("❌ No accessible OpenAI model for this API key!")

# Initialize LangChain LLM with selected model
llm = ChatOpenAI(model=selected_model, temperature=0)
