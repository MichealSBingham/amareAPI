api_key = "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"

import os
import openai
import json
openai.api_key = api_key




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
                max_tokens=555 
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




