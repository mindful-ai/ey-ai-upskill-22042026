from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from datetime import datetime
from langchain_openai import OpenAI


# from langchain_core.output_parsers import DatetimeOutputParser
from langchain_openai import ChatOpenAI


key_path = r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\openai\ne-openai-api-key.txt"
f = open(key_path)
apikey = f.read().strip()
f.close()

llm = ChatOpenAI(openai_api_key=apikey, temperature=0)


import re
from typing import Optional


class HistoryQuiz():
    
    def create_history_question(self,topic):
        '''
        This method should output a historical question about the topic that has a date as the correct answer.
        For example:
        
            "On what date did World War 2 end?"
            
        '''
        # Use LangChain PromptTemplate to generate a clear question string
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="On what date did {topic} occur?"
        )
        question = prompt.format(topic=topic)
        return question
    
    def get_AI_answer(self,question):
        '''
        This method should get the answer to the historical question from the method above.
        Note: This answer must be in datetime format! Use DateTimeOutputParser to confirm!
        
        September 2, 1945 --> datetime.datetime(1945, 9, 2, 0, 0)
        '''
        # Ask a chat model to answer with a single ISO date (YYYY-MM-DD).
        system = SystemMessagePromptTemplate.from_template(
            "You are a historian. Answer with a single date in ISO format YYYY-MM-DD. Reply with the date only, nothing else."
        )
        human = HumanMessagePromptTemplate.from_template("{question}")
        chat_prompt = ChatPromptTemplate.from_messages([system, human])

        try:
            prompt = chat_prompt.format_prompt(question=question)
            messages = prompt.to_messages()
            text = None
            # Prefer .generate when available (returns structured generations)
            if hasattr(llm, "generate"):
                try:
                    result = llm.generate([messages])
                    gens = getattr(result, "generations", None)
                    if gens:
                        # gens is a list of lists
                        text = gens[0][0].text
                    else:
                        # Try alternative attribute
                        text = str(result)
                except Exception:
                    text = None

            # Fallback to calling the model if callable
            if text is None and callable(llm):
                try:
                    response = llm(messages)
                    # Response may be an AIMessage or similar
                    if hasattr(response, "content"):
                        text = response.content
                    elif hasattr(response, "generations"):
                        text = response.generations[0][0].text
                    else:
                        text = str(response)
                except Exception:
                    text = None

            if not text:
                print("Warning: LLM did not return text or is not configured for local use.")
                return None

            # Find ISO-like date in the response
            m = re.search(r"(\d{4}-\d{2}-\d{2})", text)
            if m:
                iso = m.group(1)
                try:
                    correct_datetime = datetime.fromisoformat(iso)
                    return correct_datetime
                except Exception:
                    pass

            # Fallback: try to parse with DatetimeOutputParser if available
            try:
                parser = DatetimeOutputParser()
                parsed = parser.parse(text)
                if isinstance(parsed, datetime):
                    return parsed
            except Exception:
                pass

        except Exception as e:
            print("Warning: LLM call failed or not configured:", e)

        return None
    
    def get_user_answer(self,question):
        '''
        This method should grab a user answer and convert it to datetime. It should collect a Year, Month, and Day.
        You can just use input() for this.
        '''
        # Ask the user for a date in ISO format for simplicity
        prompt = f"{question}\nPlease enter the answer date in YYYY-MM-DD format: "
        s = input(prompt)
        try:
            user_datetime = datetime.fromisoformat(s.strip())
            return user_datetime
        except Exception:
            print("Invalid date format. Expected YYYY-MM-DD. Returning None.")
            return None
        
        
    def check_user_answer(self,user_answer,ai_answer):
        '''
        Should check the user answer against the AI answer and return the difference between them
        '''
        if user_answer is None:
            print("No valid user answer to check.")
            return None
        if ai_answer is None:
            print("No AI answer available to check against.")
            return None

        # Compute absolute difference in days
        diff = abs((user_answer - ai_answer).days)
        print(f"Difference between user answer and AI answer: {diff} day(s)")
        return diff


if __name__ == "__main__":
    # Simple example quiz flow
    hq = HistoryQuiz()
    topic = "the end of World War 2"
    question = hq.create_history_question(topic)
    print("Question:", question)

    ai_dt = hq.get_AI_answer(question)
    print("AI answer (datetime):", ai_dt)

    user_dt = hq.get_user_answer(question)
    print("User answer (datetime):", user_dt)

    hq.check_user_answer(user_dt, ai_dt)
        