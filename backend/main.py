from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, sys, pdb

from Module.BaseSolar import BaseSolar, buffer_memory

app = FastAPI()

backend_port = 8188
frontend_port = 3000

origins = [
  "http://localhost",
  f"http://localhost:{backend_port}",
  f"http://localhost:{frontend_port}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptInput(BaseModel):
  question : str

class PromptInputWithMBTI(BaseModel):
  question : str
  mbti : str

@app.post("/solar_start")
def solar_start(response : PromptInput):
  response = BaseSolar.run_solar(question=response.question)
  return response

buffer = buffer_memory()
conv_prompt = buffer['prompt']
conv_prompt2 = buffer['prompt2']
conv_prompt3 = buffer['prompt3']
conv_prompt4 = buffer['prompt4']
conv_memory = buffer['memory']
@app.post("/solar_conv_memory")
def solar_conv_memory(response : PromptInput):
  result = BaseSolar.run_solar_with_conv_memory(question=response.question, prompt=conv_prompt, memory=conv_memory)
  return result

@app.post("/solar_conv_memory2")
def solar_conv_memory2(response : PromptInput):
  result = BaseSolar.run_solar_with_conv_memory2(question=response.question, prompt=conv_prompt2, memory=conv_memory)
  return result

@app.post("/solar_conv_memory3")
def solar_conv_memory3(response : PromptInput):
  result = BaseSolar.run_solar_with_conv_memory3(question=response.question, prompt=conv_prompt3, memory=conv_memory)
  return result

@app.post("/solar_conv_memory4")
def solar_conv_memory4(response : PromptInput):
  result = BaseSolar.run_solar_with_conv_memory4(question=response.question, prompt=conv_prompt4, memory=conv_memory)
  return result

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=int(backend_port), reload=True)