import google.generativeai as genai

genai.configure(api_key="AIzaSyBuaGhLnjZOmgheEXKCDR5W9toQ4J2UjcU")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)