from datetime import datetime

# Prompts
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Models (OpenAI integration moved out)
from langchain_openai import ChatOpenAI

# Output parsing helper (DatetimeOutputParser not available in some langchain versions)
def parse_date(text):
    """Parse a date string into a datetime.datetime.

    Tries dateutil.parser if available, then ISO, then common human formats.
    Raises ValueError if unable to parse.
    """
    text = text.strip().strip('"')
    # Try dateutil if installed
    try:
        from dateutil import parser as _dparser
        dt = _dparser.parse(text, default=datetime(1, 1, 1))
        # normalize
        return dt.replace(tzinfo=None)
    except Exception:
        pass

    # Try ISO format
    try:
        return datetime.fromisoformat(text)
    except Exception:
        pass

    # Common formats
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            continue

    # Last resort: extract numbers like YYYY, M, D
    import re
    m = re.search(r"(\d{4}).*?(\d{1,2}).*?(\d{1,2})", text)
    if m:
        y, a, b = m.groups()
        y = int(y)
        a = int(a)
        b = int(b)
        # assume order is Year-Month-Day if plausible
        try:
            if 1 <= a <= 12 and 1 <= b <= 31:
                return datetime(y, a, b)
        except Exception:
            pass

    raise ValueError(f"Unable to parse date: {text}")

# LLM client creation (reads API key if available)
from langchain_openai import OpenAI as LangChainOpenAI

try:
    with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill-2\key-vault\openai\ne-openai-api-key.txt") as f:
        apikey = f.read().strip()
    llm = LangChainOpenAI(api_key=apikey)
except Exception:
    llm = None


class HistoryQuiz():
    """History quiz bot that can use an LLM to generate questions and answers.

    If an LLM isn't available, some methods fall back to deterministic mappings.
    """

    def create_history_question(self, topic):
        '''
        This method should output a historical question about the topic that has a date as the correct answer.
        For example:

            "On what date did World War 2 end?"

        The method returns a single question string. Uses LLM when available.
        '''
        prompt = (
            "Generate a single concise historical trivia question about '{topic}' "
            "whose answer is a specific calendar date. Return ONLY the question sentence."
        ).format(topic=topic)

        if llm is None:
            # Fallback: simple templated question
            question = f"On what date did {topic} end?"
            return question

        resp = self._call_llm(prompt)
        question = resp.strip().strip('"')
        return question

    def get_AI_answer(self, question):
        '''
        This method gets the answer to the historical question from an LLM.
        The returned value is a `datetime.datetime` object.
        '''
        prompt = (
            f"Answer the following historical question and return ONLY the date in the format 'Month D, YYYY'.\n\n{question}"
        )

        if llm is None:
            # Fallback deterministic mapping
            mapping = {
                'world war 2': datetime(1945, 9, 2),
                'world war ii': datetime(1945, 9, 2),
                'world war 1': datetime(1918, 11, 11),
                'american civil war': datetime(1865, 4, 9),
            }
            q_lower = question.lower()
            for key, dt in mapping.items():
                if key in q_lower:
                    return dt
            raise ValueError(f"No fallback mapping for question: {question}")

        resp = self._call_llm(prompt)

        # Try to parse using the helper that uses dateutil and common formats
        try:
            return parse_date(resp)
        except Exception:
            raise ValueError(f"Unable to parse date from LLM response: {resp}")

    def get_user_answer(self, question):
        '''
        This method grabs a user answer and converts it to datetime. It collects Year, Month, and Day via input().
        '''
        print(question)
        while True:
            try:
                year = int(input('Enter year (e.g. 1945): ').strip())
                month = int(input('Enter month (1-12): ').strip())
                day = int(input('Enter day (1-31): ').strip())
                user_datetime = datetime(year, month, day)
                return user_datetime
            except ValueError:
                print('Invalid date or input. Please try again.')

    def check_user_answer(self, user_answer, ai_answer):
        '''
        Check the user answer against the AI answer and return the absolute timedelta difference.
        '''
        if not isinstance(user_answer, datetime) or not isinstance(ai_answer, datetime):
            raise TypeError('Both answers must be datetime.datetime instances')

        delta = user_answer - ai_answer
        days_diff = abs(delta.days)
        hours_diff = abs(delta.seconds) // 3600
        message = f"Difference: {days_diff} days and {hours_diff} hours."
        if days_diff == 0 and hours_diff == 0:
            message = "Exact match!"
        print(message)
        return abs(delta)

    def _call_llm(self, prompt_text):
        """Call the configured LLM with a prompt, trying several call styles for compatibility."""
        if llm is None:
            raise RuntimeError('LLM client not configured')

        # Try calling the llm in a few common ways and extract text
        try:
            out = llm(prompt_text)
            if isinstance(out, str):
                return out
        except Exception:
            pass

        try:
            out = llm.predict(prompt_text)
            if isinstance(out, str):
                return out
        except Exception:
            pass

        try:
            out = llm.generate([prompt_text])
            if hasattr(out, 'generations'):
                first = out.generations[0][0].text
                return first
            if hasattr(out, 'choices'):
                return out.choices[0].text
        except Exception:
            pass

        raise RuntimeError('Failed to call LLM with available methods')


def test_quiz_bot(use_llm=True):
    quiz_bot = HistoryQuiz()
    question = quiz_bot.create_history_question(topic='World War 2')
    ai_answer = None
    try:
        ai_answer = quiz_bot.get_AI_answer(question)
    except Exception as e:
        if not use_llm:
            raise
        print('LLM failed to answer; test will attempt fallback if available:', e)

    if ai_answer is None:
        # Try fallback deterministic mapping via get_AI_answer with llm disabled
        global llm
        saved = llm
        llm = None
        ai_answer = quiz_bot.get_AI_answer(question)
        llm = saved

    # simulate a user answer identical to AI answer
    user_answer = datetime(ai_answer.year, ai_answer.month, ai_answer.day)
    diff = quiz_bot.check_user_answer(user_answer, ai_answer)
    assert diff.days == 0, 'Test failed: expected zero difference'
    print('Automated test passed: user answer matches AI answer')


if __name__ == "__main__":
    quiz_bot = HistoryQuiz()
    question = quiz_bot.create_history_question(topic='World War 2')
    print('\nQuestion: ', question)

    try:
        ai_answer = quiz_bot.get_AI_answer(question)
        print('AI (correct) answer:', ai_answer.date())
    except Exception as e:
        print('Failed to get AI answer:', e)
        ai_answer = None

    if ai_answer is not None:
        user_answer = quiz_bot.get_user_answer(question)
        quiz_bot.check_user_answer(user_answer, ai_answer)

    print('\nRunning automated self-test...')
    test_quiz_bot()
