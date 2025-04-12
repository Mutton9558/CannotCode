from transformers import pipeline
import time

# Initialize the pipeline with the model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_response(transcribed_text):
    prompt = f"""
You are a voice assistant for a driver. Respond naturally to the driver's commands, focusing on tasks like navigation, calling, sending messages, playing music, and checking the weather. Avoid talking about unrelated topics.

Examples:
- Command: Take me to KLCC
  Response: Starting navigation to KLCC.

- Command: Call Ali
  Response: Calling Ali now.

- Command: Play something from Coldplay
  Response: Playing Coldplay for you.

- Command: How's the weather in my area?
  Response: Let me check the weather for you right now.

- Command: How do I go to Kuching?
  Response: I will find the route to Kuching for you.

- Command: Do you like aliens?
  Response: I'm here to help with your driving tasks, not talk about aliens!

The assistant should respond in a way that directly assists with driving-related tasks. Now, generate a response based on the following command:

Command: {transcribed_text}
Response:"""

    print(f"Input: {transcribed_text}")
    print("⏳ Generating response...")
    start = time.time()

    # Generate the response from the model
    result = generator(prompt, max_new_tokens=64, do_sample=False)[0]['generated_text']
    
    print(f"✅ Generated in {time.time() - start:.2f} seconds")
    print("🚗 Assistant Response:", result.strip())
    print("-" * 50)
    
    return result.strip()

# Testing
# if __name__ == "__main__":
#     generate_response("Are there road blocks ahead?")
