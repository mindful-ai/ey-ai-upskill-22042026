class HistoryQuiz():
    
    def create_history_question(self, topic):
        '''
        This method should output a historical question about the topic that has a date as the correct answer.
        For example:
        
            "On what date did World War 2 end?"
            
        '''
        # System Prompt
        system_template = "You write a single quiz question about {topic}. You return only the question."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        # Human Request
        human_template = "{question_request}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # Compile to Chat
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # Insert the variables
        request = chat_prompt.format_prompt(topic=topic, question_request="Give me a quiz question where the correct answer is a specific date").to_messages()

        # Make the request
        chat = ChatOpenAI(api_key=apikey)
        result = chat.invoke(request)
       
        return result.content
    
    def get_AI_answer(self,question):
        '''
        This method should get the answer to the historical question from the method above.
        Note: This answer must be in datetime format! Use DateTimeOutputParser to confirm!
        
        September 2, 1945 --> datetime.datetime(1945, 9, 2, 0, 0)
        '''

        output_parser = DatetimeOutputParser()

        # System template
        system_template = "You answer the quiz question with just a date"
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        # Human Template
        human_template = '''Answer the user question: 
        {question}   

        Instructions for you ->
        {instructions}'''
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # Compile to chat
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # Insert the generated question and format the instructions
        request = chat_prompt.format_prompt(question=question, instructions=output_parser.get_format_instructions()).to_messages()

        # Make the request
        chat = ChatOpenAI(api_key=apikey)
        result = chat.invoke(request)

        correct_datetime = output_parser.parse(result.content)
        
        return correct_datetime
    
    def get_user_answer(self,question):
        '''
        This method should grab a user answer and convert it to datetime. It should collect a Year, Month, and Day.
        You can just use input() for this.
        '''
        
        print(question)

        year = int(input("Enter the year: "))
        month = int(input("Enter the month: "))
        day = int(input("Enter the day: "))

        user_datetime = datetime(year, month, day)
        
        return user_datetime
        
        
    def check_user_answer(self,user_answer,ai_answer):
        '''
        Should check the user answer against the AI answer and return the difference between them
        '''
        # print or return the difference between the answers here!
        result = user_answer - ai_answer
        print("The difference between dates: ", result)
        
