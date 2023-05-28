import openai
import time 
# TODO LIST:
# - Restart chat if client asks to end
# - Let free-petto roam google/bing for answers
# - 
# - Add 
  

class ChatAssistant:
    def __init__(self, api_key, input_prompt="You are a helpful assistant.", model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.input_prompt = input_prompt
        self.conversation_history = []
        self.restart_conversation()
        self.last_time = time.time() # time in seconds
        self.history_time_window = 30*60 # time in seconds
        openai.api_key = api_key


    def restart_conversation(self):
        self.conversation_history = [{"role": "system", "content": self.input_prompt}]
    
    def check_time(self):
        new_time = time.time()
        if new_time-self.last_time> self.history_time_window:
            self.restart_conversation()

        self.last_time = new_time       

    async def generate_chat_response(self, message):

        new_time = time.time()
        if new_time-self.last_time> self.history_time_window:
            self.restart_conversation()

        self.last_time = new_time

        conversation = self.conversation_history + [{"role": "user", "content": message.content}]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=conversation,
        )

        response_text = response.choices[0].message.content.strip()
        self.conversation_history.extend([
            {"role": "user", "content": message.content},
            {"role": "assistant", "content": response_text},
        ])

        return response_text

    def reset_conversation(self):
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]