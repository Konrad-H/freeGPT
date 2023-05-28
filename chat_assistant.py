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
        self.chat_histories = {}
        self.last_time = {} # time in seconds
        self.history_time_window = 30*60 # time in seconds
        openai.api_key = api_key

    def get_unique_key(self, message):
        return f"{message.guild.id}_{message.channel.id}_{message.author.id}"

    def get_conversation_history(self, key):
        return self.chat_histories.get(key, [])

    def set_conversation_history(self, key, history):
        self.chat_histories[key] = history

    def restart_conversation(self, key):
        self.chat_histories[key] = [{"role": "system", "content": self.input_prompt}]

    def check_time_and_reset(self, key):
        new_time = time.time()

        if key not in self.last_time:
            self.last_time[key] = new_time
            return new_time
 
        elif new_time - self.last_time[key] > self.history_time_window:
            self.restart_conversation(key)
            return new_time

    async def generate_chat_response(self, message):

        unique_key = self.get_unique_key(message)
        self.check_time_and_reset(unique_key)
        conversation_history = self.get_conversation_history(unique_key)

        conversation = conversation_history + [{"role": "user", "content": message.content}]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=conversation,
        )

        response_text = response.choices[0].message.content.strip()
        conversation_history.extend([
            {"role": "user", "content": message.content},
            {"role": "assistant", "content": response_text},
        ])

        self.set_conversation_history(unique_key, conversation_history)

        return response_text