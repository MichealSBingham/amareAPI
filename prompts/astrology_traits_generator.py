api_key = "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"

import os
import openai
from openai import OpenAI
import json
openai.api_key = api_key
client = OpenAI( api_key=api_key )
DASHA_ASSISTANT_ID = "asst_oh3BtBECBD1cqa3VidCPbk2t"
from database.user import User

from prompts.constants import *
from Messaging.streamBackend import * 
from database.user import db

# TODO: make sure it can handle placements on cusps 
class PlacementInterpretationsGenerator:
    
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.instructions = PREDICTING_PLANETARY_PLACEMENT
        self.messages = []
        self.prompt = ""

    # example: male, sun, cancer, 7th. be sure the house number 
    def _format_request_message(self,  gender, planet, sign, house=''):
        if not house or house.isspace():
            message = f"I'm a {gender} with {planet} in {sign}. Tell me about myself. Do NOT mention the name of the placement until the end of the reading, towards the end you can speak more about the reasoning behind it such as the planet, sign, and house, but in the beginning just tell me my reading nothing else. "
        else: 
            message = f"I'm a {gender} with {planet} in {sign} in the {house} house. Tell me about myself. Do NOT mention the name of the placement until the end of the reading, towards the end you can speak more about the reasoning behind it such as the planet, sign, and house, but in the beginning just tell me my reading nothing else. "
        self.prompt = message 
        return message.strip()
    

    def interpret_placement(self, gender, planet, sign, house):
        request_message = self._format_request_message(gender, planet, sign, house)
        print(f"the message sent is ... {request_message}")
        
        
        outbound_messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": request_message}
            ]
            
        response = openai.ChatCompletion.create(
                model=self.model,
                messages=outbound_messages, 
                temperature=0, # adjust this value as needed
                max_tokens=1000, 
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        response_content = response.choices[0].message['content'].strip()
        return response_content

          
        
    


class PersonalityStatementsGenerator: 
    def __init__(self, max_retries=3):
        from prompts.constants import PREDICTING_STATEMENTS_INTRUCTIONS
        self.model = "gpt-3.5-turbo-16k"
        self.instructions = PREDICTING_STATEMENTS_INTRUCTIONS
        self.messages = []
        self.max_retries = max_retries

    def _format_request_message(self, name, gender, astro_data):
        message = f"predict statements of the following person\n\n{name}\n{gender}\n"
        for key, value in astro_data.items():
            message += f"{key}: {value}\n"
        return message.strip()
    
    # Some Utilites...

    def split_statements(self, text, delimiter='+'):
        statements = text.split(delimiter)
        result = []
        temp = ""
        for statement in statements:
            temp += statement
            if temp.endswith('.'):
                result.append(temp.strip().strip('\n'))
                temp = ""
            else:
                temp += delimiter
        return result

# not sure if this is working so well... may need to fall back to deprecated functions i think it has to do with the statement parser
    def predict_statements(self, name, gender, astro_data):
        for attempt in range(3):
            try:
                request_message = self._format_request_message(name, gender, astro_data)

                outbound_messages = [
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": request_message}
                ]

                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=outbound_messages,
                    temperature=0.45,
                    max_tokens=250
                )
                response_content = response.choices[0].message['content']
                
                result = self.split_statements(response_content)
                
                if result:
                    return result
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        return []

    def predict_statements_old(self, name, gender, astro_data):
        request_message = self._format_request_message(name, gender, astro_data)
        
    
        
        outbound_messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": request_message}
            ]
            
        response = openai.ChatCompletion.create(
                model=self.model,
                messages=outbound_messages, 
                temperature=0.45, # adjust this value as needed
                max_tokens=250 # 300 might be a little better
            )
        response_content = response.choices[0].message['content']
        print(response_content)
        return response_content #self.split_statements(response_content)

          

class AstrologyTraitsGenerator:
    def __init__(self, max_retries=3):
        from prompts.constants import PREDICTING_TRAITS_INSTRUCTIONS

        self.model = "gpt-3.5-turbo-16k"
        self.instructions = PREDICTING_TRAITS_INSTRUCTIONS
        self.messages = []
        self.max_retries = max_retries

    def _format_request_message(self, name, gender, astro_data):
        message = f"predict the traits of the following person\n\n{name}\n{gender}\n"
        for key, value in astro_data.items():
            message += f"{key}: {value}\n"
        return message.strip()


    


    def _validate_traits(self, response):
        traits_list = response.split(", ")
        
        # Convert traits list to dictionary
        traits_dict = {}
        for trait in traits_list:
            try:
                trait_value, likelihood = trait.split(":")
                traits_dict[trait_value] = likelihood
            except ValueError:
                # if it can't split into exactly two parts, it's invalid
                return False, {}

        # You can add further validation checks here if needed

        return True, traits_dict


    def predict_traits(self, name, gender, astro_data):
        request_message = self._format_request_message(name, gender, astro_data)
        
        retry_count = 0
        while retry_count < self.max_retries:
            outbound_messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": request_message}
            ]
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=outbound_messages, 
                temperature=0.45, # adjust this value as needed
                max_tokens=100  #we can go a bit lower here
            )
            response_content = response.choices[0].message['content']
            is_valid, traits_dict = self._validate_traits(response_content)

            if is_valid:
                return traits_dict  # return the results immediately if valid

            retry_count += 1  # increment retry count if not valid

        return {}  # return an empty dictionary if max_retries is exceeded


    


    def _save_chat(self):
        chat_data = {
            "instructions": self.instructions,
            "model": self.model
        }
        with open('chat_history.json', 'w') as f:
            json.dump(chat_data, f, indent=4)



class DashaChatBot:
    
    ## Creates the initial thread and sends the welcome message to the user 
    @staticmethod
    def createInitialThread(userID): 
        """ Creates the initial thread and sends the welcome message to the user and sends the thread id to the user database"""

        

        thread = client.beta.threads.create(
            messages=[
                
                 {
                "role": "user",
                    "content": "Hi. Introduce yourself"
                
                 }
                    ]
            )
        
        promptForUser = User(id=userID).chartSummaryForPrompt()
        
        run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=DASHA_ASSISTANT_ID,
                instructions=f"{DASHA_PROMPT} {promptForUser}"
                    )
        
        while run.status !="completed":
            run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
                                )
            
        print(run.status)

        messages = openai.beta.threads.messages.list(
                 thread_id=thread.id
        )

        # Update thread ID in firebase now
        db.collection('users').document(userID).update({'dashaThreadID': thread.id})
        
        response = messages.data[0].content[0].text.value
        send_welcome_message(userID, response)

        print(messages.data[0].content[0].text.value)


    @staticmethod
    def sendMessageFrom(userID, message): 
        user = User(id=userID)
        
        dashaThreadID = user.dashaThreadID 
        
        thread_message = client.beta.threads.messages.create(
            dashaThreadID,
            role="user",
            content=message,
                )
        
        promptForUser = User(id=userID).chartSummaryForPrompt()
        
        run = client.beta.threads.runs.create(
                thread_id=dashaThreadID,
                assistant_id=DASHA_ASSISTANT_ID,
                instructions=f"{DASHA_PROMPT} {promptForUser}"
                    )
        
        while run.status !="completed":
            run = openai.beta.threads.runs.retrieve(
            thread_id=dashaThreadID,
            run_id=run.id
                                )
        print(run.status)

        messages = openai.beta.threads.messages.list(
                 thread_id=dashaThreadID
        )

        response = messages.data[0].content[0].text.value

        send_message_to_user(userID, response)


       
