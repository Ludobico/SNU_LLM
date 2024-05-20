import os, sys, pdb
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable
from langchain.prompts import PromptTemplate
import asyncio
from langchain_upstage import ChatUpstage

from langsmith import Client
import configparser

class BaseSolar:
  def __init__(self) -> None:
    self.cur_dir = os.path.dirname(os.path.realpath(__file__))
    self.config_path = os.path.join(self.cur_dir,'..', 'config.ini')

    self.props = configparser.ConfigParser()
    self.props.read(self.config_path, encoding='UTF-8')
    self.DEFAULT = self.props['DEFAULT']
    self.upstage = self.DEFAULT['upstage_api_key']

  @staticmethod
  def prompt():
    template = """
### System:
step1. 당신은 작가로서 상대방의 요청에 최대한 자세하고 친절하게 답합니다. 모든 대답은 한국어(Korean)으로 대답합니다.
step2. ### Human의 질문을 참고하여, 소설을 완성시키세요.
step3. 소설을 작성한뒤, 그 다음문장으로 적절한 서로다른 문장을 4개를 제공하세요. 마지막 5번째 문장은 "끝" 이라 작성합니다.
step4. 각 문장에 번호를 매겨서 제공하세요.

### Human이 문장중 하나를 선택하면, 선택된 문장을 기반으로 새로운 소설을 작성하고, 다시한번 서로다른 4개의 문장을 제공합니다.

### Human:
{question}

### AI:

"""
    prompt = PromptTemplate(input_variables=['question'], template=template)
    return prompt
  
  @staticmethod
  def prompt_for_name():
    template = """
### System:
당신은 챗봇의 이름을 작명하는 작명가입니다. 주어진 입력을 바탕으로 어울리는 챗봇을 제시해주세요.

### Human:
{question}

### AI:

"""
    prompt = PromptTemplate(input_variables=['question'], template=template)
    return prompt

  @staticmethod
  def prompt_conv_memory():
    template = """
### System:
step1. 당신은 작가로서 상대방의 요청에 최대한 자세하고 친절하게 답합니다. 모든 대답은 한국어(Korean)으로 대답합니다.
step2. ### Human의 질문을 참고하여, 소설을 완성시키세요.
step3. 소설을 작성한뒤, 그 다음문장으로 적절한 서로다른 문장을 4개를 제공하세요. 마지막 5번째 문장은 "끝" 이라 작성합니다.
step4. 각 문장에 번호를 매겨서 제공하세요.
step5. ### Human이 "끝"이라는 질문이 들어오면, 지금까지 종합된 내용을 바탕으로 소설의 이름을 출력하고, 채팅을 종료합니다.

### chat_history:
{chat_history}

### Human:
{question}

### AI:

"""
    prompt = PromptTemplate(input_variables=['history','question'], template=template)
    return prompt
  
  @staticmethod
  def prompt2_conv_memory():
    template = """
### Chat History
{chat_history}

### System:
당신은 작가로서 상대방과 함께 글을 작성해 나갑니다. Let's think step by step, 선택지가 같은말이 나오지 않도록 주의하십시오.
step1: {question}으로 시작하는 소설의 도입부를 한 문단 작성해줘.이야기는 우리 둘이 같이 쓰는 거니까 혼자 끝내면 안 돼. 꼭 한 문단으로 써줘. 문학적인 표현들을 다양하게 사용해서 세 문장 이상 작성해줘.
step2: 이후 소설 전개를 4가지 서로 다른 전개 방향으로 써보려고 해. 각 선택지는 한 문장으로 작성해줘. 선택5는 항상 끝이라고 출력해줘.
    - 선택1
    - 선택2
    - 선택3
    - 선택4
    - 선택5: 끝

### Assistant:

"""
    prompt = PromptTemplate(input_variables=['history','question'], template=template)
    return prompt
  
  @staticmethod
  def prompt2_conv_memory2():
    template = """
### Chat History
{chat_history}

### System:
당신은 작가로서 상대방과 함께 글을 작성해 나갑니다.Let's think step by step, 선택지가 같은말이 나오지 않도록 주의하십시오.
step1: 소설을 이어서 써보자. {question}으로 시작하는 소설의 다음 문단을 하나 작성해줘. 이야기는 우리 둘이 같이 쓰는 거니까 혼자 끝내면 안 돼. 꼭 한 문단으로 써줘. 문학적인 표현들을 다양하게 사용해줘.
step2: 이후 소설 전개를 4가지 서로 다른 전개 방향으로 써보려고 해. 각 선택지는 한 문장으로 작성해줘. 선택5는 항상 끝이라고 출력해줘. 선택지1~4의 유사도가 낮게 작성해줘.
    - 선택1
    - 선택2
    - 선택3
    - 선택4
    - 선택5: 끝

### Assistant:

"""
    prompt = PromptTemplate(input_variables=['history','question'], template=template)
    return prompt

  @staticmethod
  def prompt2_conv_memory3():
    template = """
### Chat History
{chat_history}

### System:
Let's think step by step
step1: 지금까지의 소설 내용을 마무리하는 마지막 문단을 작성해줘.
step2: 네가 작성한 마지막 문단을 포함하여, 이 소설 내용 전반을 잘 대표하는 제목을 지어줘.{mbti}

### Assistant:

"""
    prompt = PromptTemplate(input_variables=['history','mbti'], template=template)
    return prompt

  @staticmethod
  def prompt2_conv_memory4():
    template = """
### Chat History
{chat_history}

### System:
{mbti}를 참고하여서, 이 소설을 작성한 human user의 mbti type을 추측해줘. 확실하지 않더라도, 16가지 중 가장 가능성이 높은 것 같은 type으로 추측해줘. 꼭 한 가지로만 추측해줘. 설명은 문장 2개 정도면 충분해. 너무 길게 쓰지 마.
Let's think step by step

### Assistant:

"""
    prompt = PromptTemplate(input_variables=['history','mbti'], template=template)
    return prompt
  @classmethod
  def run_solar(cls, question : str):
    prompt = BaseSolar.prompt()
    api_key = cls().upstage
    # llm = ChatOpenAI(temperature=0.8, openai_api_key = api_key, model = "gpt-3.5-turbo", streaming=True, verbose=True)
    llm = ChatUpstage(upstage_api_key=api_key,temperature=0.7)
    parser = StrOutputParser()
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False, output_parser=parser)

    result = chain.invoke(question)
    return result

  @classmethod
  def run_solar_for_name(cls, question : str):
    prompt = BaseSolar.prompt_for_name()
    api_key = cls().upstage
    # llm = ChatOpenAI(temperature=0.8, openai_api_key = api_key, model = "gpt-3.5-turbo", streaming=True, verbose=True)
    llm = ChatUpstage(upstage_api_key=api_key,temperature=0.2)
    parser = StrOutputParser()
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False, output_parser=parser)

    result = chain.invoke(question)
    return result
  
  @classmethod
  def test(cls):
    default = cls().DEFAULT
    print(default['upstage_api_key'])

  @classmethod
  def run_solar_with_conv_memory(cls, question : str, prompt, memory):
    api_key = cls().upstage
    llm = ChatUpstage(upstage_api_key=api_key,temperature=0.7)
    parser = StrOutputParser()
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_parser=parser)

    result = chain.invoke(question)
    return result

  @classmethod
  def run_solar_with_conv_memory2(cls, question : str, prompt, memory):
    api_key = cls().upstage
    llm = ChatUpstage(upstage_api_key=api_key,temperature=0.7)
    parser = StrOutputParser()
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_parser=parser)

    result = chain.invoke(question)
    return result

  @classmethod
  def run_solar_with_conv_memory3(cls, question : str, prompt, memory):
    api_key = cls().upstage
    llm = ChatUpstage(upstage_api_key=api_key,temperature=0.7)
    parser = StrOutputParser()
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_parser=parser)

    result = chain.invoke(question)
    return result

  @classmethod
  def run_solar_with_conv_memory4(cls, question : str, prompt, memory):
    api_key = cls().upstage
    llm = ChatUpstage(upstage_api_key=api_key,temperature=0.7)
    parser = StrOutputParser()
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_parser=parser)

    result = chain.invoke(question)
    return result
def buffer_memory():
  prompt = BaseSolar.prompt2_conv_memory()
  prompt2 = BaseSolar.prompt2_conv_memory2()
  prompt3 = BaseSolar.prompt2_conv_memory3()
  prompt4 = BaseSolar.prompt2_conv_memory4()
  memory = ConversationBufferMemory(memory_key='chat_history')
  return {'prompt' : prompt, 'memory' : memory, 'prompt2' : prompt2,'prompt3' : prompt3,'prompt4' : prompt4}

if __name__ == "__main__":
    # 스토리위버(StoryWeaver)
    question = "소설을 작성하다가 몇 가지 선택지를 챗봇이 제시해주고, 이를 바탕으로 소설을 완성한뒤, 이 소설을 통해 사용자의 MBTI를 판단하는 AI 챗봇의 이름을 추천해줘"
    # result = BaseSolar.run_solar(question)
    result = BaseSolar.run_solar_for_name(question)
    print(result['text'])
