
# Custom memory class to work with your Gemini client
class CustomMemoryBuffer:
    def __init__(self, max_token_limit=1000):
        self.memory = []
        self.max_token_limit = max_token_limit

    def add(self, content):
        self.memory.append(content)
        # Implement token counting and truncation logic here if needed
        # For simplicity, we're just keeping a fixed number of recent items
        if len(self.memory) > 5:
            self.memory = self.memory[-5:]

    def get(self):
        return "\n\n".join(self.memory)