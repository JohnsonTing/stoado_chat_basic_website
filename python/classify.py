from flask import Flask, request, jsonify
from flask_cors import CORS

import re

import requests


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

api_key = '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'

#--------------------------------------------------------------------------------
#Function to check for platform leakage, manualFilter.py

# List of keywords and phrases to block for platform leakage
leakage_keywords = [
    "email", "phone number", "whatsapp", "telegram", "skype", "viber", "signal",
    "wechat", "line", "facebook", "messenger", "instagram", "twitter", "linkedin",
    "snapchat", "discord", "zoom", "google meet", "email me at", "call me at", 
    "text me at", "contact me at", "reach me at", "dm me", "pm me", "direct message", 
    "private message", "send me a message", "send an email", "phone", "mobile", "cell", 
    "cellphone", "number", "digit", "handle", "user name", "username", "profile", "id", 
    "account", "at", "dot", "com", "txt", "gram", "snap", "link", "social", "meet", 
    "chat", "outside", "another platform", "different platform", "external site", 
    "external platform", "offsite", "off-site", "other site", "off platform", "out of platform", 
    "bank", "bnk", "whatspp", "07", "@", "selling fees", "eBay", "ebay", "amazon", "fb marketplace", "depop", "ring me"
    ,"bell me"
]

# Regular expressions for email, phone number, and address
email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
phone_pattern = re.compile(r'(\+?\d{1,3}[.\s-]?)?(\(?\d{3}\)?[.\s-]?)?[\d\s.-]{7,10}')


address_pattern = re.compile(
    r'\b(\d{1,5}\s(?:[A-Za-z0-9.\-]+\s){1,5}(?:Street|road|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Lane|Ln|Court|Ct|Circle|Cir|Place|Pl|Square|Sq|Trail|Trl|Parkway|Pkwy|Commons))\b'
    r'|\b(\d{1,5}\s(?:[A-Za-z0-9.\-]+\s){1,5}(?:[A-Z][a-z]+,?\s[A-Z]{2}\s\d{5}))\b'
    r'|\b(?:P\.?\s?O\.?\s?Box\s?\d{1,6})\b'
)

def check_platform_leakage(message):
    # Check for keywords
    for keyword in leakage_keywords:
        if keyword in message.lower():
            return True  # Keyword found, message is prohibited
    
    # Check for email addresses
    if email_pattern.search(message):
        return True  # Email address found, message is prohibited
    
    # Check for phone numbers
    if phone_pattern.search(message):
        return True  # Phone number found, message is prohibited

    # Check for addresses
    if address_pattern.search(message):
        return True  # Address found, message is prohibited

    return False  # No prohibited content found

#------------------------------------------------------------------------------
#function to check for offensive language, offenseCheckerV2.py

def check_offensive_language(message):
    prompt = f"Check if the following message contains offensive language:\n\n{message}\n\nResponse:"
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    #Post to chat to see if offensive
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with OpenAI API: {e}")
        return False  # If there's an error with the API, treat as non-offensive to avoid blocking due to API errors

    result = response.json()

    content = result['choices'][0]['message']['content']
    print("ChatGPT Response:", content)

    return 'yes' in content.lower()



@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    message = data['message']

    if check_platform_leakage(message) and check_offensive_language(message):
        result = 'platform leakage and offensive, not sent'
    elif check_platform_leakage(message):
        result = 'platform leakage but not offensive, still not sent'
    elif check_offensive_language(message):
        result = 'not platform leakage but offensive, still not sent'
    else:
        result = 'Good message. Sent.'
    
    print(result)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(port=5000)
