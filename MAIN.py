from fastapi import FastAPI, HTTPException
import openai
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import traceback

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

openai.api_key = api_key


app = FastAPI()

prompt_template = "You are a helpful assistant. Answer the question: {question}"
prompt = PromptTemplate(input_variables=["question"], template=prompt_template)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
llm_chain = prompt | llm
@app.get("/chat")
async def chat(questio n: str):
    try:
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        response = llm_chain.invoke({"question": question})
        return {"response": response}

    except Exception as e:
        print("🔥 Error in /chat API:", traceback.format_exc())  # Debugging logs
        raise HTTPException(status_code=500, detail=str(e))
