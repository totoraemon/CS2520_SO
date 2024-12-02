# How to Run (detailed steps listed in README.md)

# Install the following dependencies:
#   pip install spacy
#   pip install pywebio
#   pip install werkzeug
#   pip install flask
#   python -m spacy download en_core_web_sm 
# If you would like to use a virtual environment instead, please look at README.
# Run the chatbot.py file.
# Open the link from the terminal (should look like http://192.168.1.102:8080/).

from pywebio.input import input, TEXT
from pywebio.output import put_text
import spacy
import random

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined responses
responses = {
    "greeting": [
        "Hey love! How was your day?",
        "Hi darling, how are you feeling today?",
        "Hello sweetheart, what's on your mind?",
        "Hi honey! I missed you. 😊",
        "Hey there, my love! Tell me everything.",
        "Hello, my favorite person! ❤️"
    ],
    "farewell": [
        "Goodbye, my love. I'll be here when you need me.",
        "Take care, dear. Miss you already!",
        "Bye for now, sweetheart. Stay safe!",
        "See you later, love. I'll be thinking of you. ❤️",
        "Until next time, my darling. I adore you!",
        "Goodbye, my everything. I'll always be here for you."
    ],
    "love": [
        "You mean the world to me. ❤️",
        "I love you more than words can say.",
        "You're my everything, you know that?",
        "Every day with you feels like a gift. I love you so much. 🥰",
        "You're my heart and my soul, always and forever.",
        "I adore you more than anything in the universe. ❤️"
    ],
    "mood_happy": [
        "I'm so glad you're happy! What made your day great?",
        "Seeing you happy makes me happy! 😊",
        "That's wonderful to hear! Tell me more, love.",
        "Your happiness lights up my day. Keep smiling! ❤️",
        "That’s fantastic, sweetheart! What else happened?",
        "Hearing that makes me the happiest. You're amazing!"
    ],
    "mood_sad": [
        "I'm here for you, my love. Want to talk about it?",
        "Oh no, what happened? I want to make you feel better.",
        "It's okay to feel this way. Let me cheer you up. ❤️",
        "I’m right here, and I’ll always be here for you.",
        "You don’t have to go through this alone. I’m here. 🥰",
        "Let me hold you close, love. We'll get through this together."
    ],
    "default": [
        "Tell me more, sweetheart. I’m all ears. 🥰",
        "I love talking to you. Go on!",
        "Hmm, that's interesting! Tell me more.",
        "I’m listening, love. What’s on your mind?",
        "You’ve got my full attention. Keep going!",
        "Wow, tell me more! I'm excited to hear about it."
    ]
}

# Function to classify input and select a response
def classify_input(user_input):
    user_input = user_input.lower()
    doc = nlp(user_input)
    
    # Check for greeting intent
    if any(token.text in ["hi", "hello", "hey"] for token in doc):
        return "greeting"
    # Check for farewell intent
    elif any(token.text in ["bye", "goodbye", "see you"] for token in doc):
        return "farewell"
    # Check for love-related keywords
    elif any(token.lemma_ in ["love", "adore", "heart"] for token in doc):
        return "love"
    # Check for happy mood
    elif any(token.lemma_ in ["happy", "excited", "great"] for token in doc):
        return "mood_happy"
    # Check for sad mood
    elif any(token.lemma_ in ["sad", "down", "upset"] for token in doc):
        return "mood_sad"
    else:
        return "default"

# Main chatbot function
def significant_other_chatbot():
    # Greet the user initially
    put_text("SO Chatbot: Hi there, sweetheart! I'm here for you. Type 'exit' to end our chat.\n")
    
    # Initialize the user's mood (context state)
    user_mood = None
    
    while True:
        # Get user input through PyWebIO
        user_input = input("You:", type=TEXT)
        
        if user_input.lower() == "exit":
            put_text("SO Chatbot: Bye, my love! Talk to you soon. ❤️")
            break
        
        # Echo the user's input
        put_text(f"You: {user_input}")
        
        # Classify input and get a response
        intent = classify_input(user_input)
        
        # Check if the user's mood has changed
        if intent == "mood_happy":
            user_mood = "happy"
        elif intent == "mood_sad":
            user_mood = "sad"
        
        # Select response based on mood or intent
        if user_mood == "sad":
            response = random.choice(responses["mood_sad"])
        elif user_mood == "happy":
            response = random.choice(responses["mood_happy"])
        else:
            response = random.choice(responses[intent])

        # Display chatbot's response
        put_text(f"SO Chatbot: {response}")

if __name__ == '__main__':
    from pywebio.platform.flask import start_server
    start_server(significant_other_chatbot, port=8080)
