import requests


URL = "https://ausopenai.azure-api.net/openai/deployments/gpt-35-turbo-16k/chat/completions?api-version=2023-07-01-preview"
KEY = "<Use your own>"

def call_openai_api(pretext,text):

    url = URL
    headers = {
        "Content-Type": "application/json",
        "api-key": KEY
    }
    data = {
        "temperature": 0.65,
        "top_p": 0.85,
        "messages" : [
            
            { 
                "role":"user", 
                "content": pretext + text 
            }
            
            ]
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    if(response.status_code!=200): 
        raise Exception(" Rate Limiting Error")
    

    return response.json()["choices"][0]["message"]["content"]