import openai

# TODO LIST:
# - Restart chat if client asks to end
# - Let free-petto roam google/bing for answers
# - 
# - Add simple Restart functionality so the main app can restart when needed
# - Add 
  

class ChatAssistant:
    def __init__(self, api_key, input_prompt="You are a helpful assistant.", model="gpt-4"):
        self.api_key = api_key
        self.model = model
        self.input_prompt = input_prompt
        self.conversation_history = [{"role": "system", "content": input_prompt}]
        openai.api_key = api_key

    async def generate_chat_response(self, input_text):
        conversation = self.conversation_history + [{"role": "user", "content": input_text}]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=conversation,
        )

        response_text = response.choices[0].message.content.strip()
        self.conversation_history.extend([
            {"role": "user", "content": input_text},
            {"role": "assistant", "content": response_text},
        ])

        return response_text

    def reset_conversation(self):
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]