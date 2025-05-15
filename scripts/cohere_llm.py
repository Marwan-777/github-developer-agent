import os
import cohere
from dotenv import load_dotenv
load_dotenv() 

keys = [os.getenv('cohere_llm_key1'), os.getenv('cohere_llm_key2'), os.getenv('cohere_llm_key3')]
generation_model = cohere.ClientV2(keys[0])
pos = 0
cnt = 0

# This function is to iterate the API Keys as a work arround to use free trial 
def check_keys():
    global generation_model, cnt, pos
    if cnt == 20:
        pos +=1
        generation_model = cohere.Client(keys[pos%3])  
        cnt = 1
    else:
        cnt += 1

# Function to generate output from a LLM 
def generate(query):
    check_keys()
    try:
        response = generation_model.chat(
            model='command-r-plus-08-2024',  
            messages= [{'role':'chatbot','content': query}]
        )
    except Exception as e:
        print('Error occured when generating text with exception: ', e)
        return None
    return response.message.content[0].text

def generate_stream(query):
    check_keys()
    response = generation_model.chat_stream(
        
            model='command-r-plus-08-2024',  
            messages= [{'role':'chatbot','content': query}]
        )
    for event in response:
        if event:
            if event.type == "content-delta":
                yield event.delta.message.content.text



query = """
Given this query between triple backticks:
I need to create a code that takes the link of an image and save the image as png locally with the following name "test_img" and save the script with the name "image_utilities" and push it to the repo 
I need the code to be in a function so if you find a script with that name just add the function to the script

and you got these set of functions to use and no need to import them:
" 
[{'name': 'push_file', 'attributes': [{'name': 'file_path', 'type': 'str'}, {'name': 'file_content', 'type': 'str'}, {'name': 'commit_msg', 'type': 'str'}], 'return type': 'No Type', 'desc': 'Takes a file path and content and push to github'}, {'name': 'update_file', 'attributes': [{'name': 'file_path', 'type': 'str'}, {'name': 'new_content', 'type': 'str'}], 'return type': 'No Type', 'desc': 'Takes a file path and new content and push the updates'}, {'name': 'get_file_content', 'attributes': [{'name': 'file_path', 'type': 'str'}], 'return type': 'str', 'desc': 'Takes a file path gets its content to modify it'}, {'name': 'file_exists', 'attributes': [{'name': 'file_path', 'type': 'str'}], 'return type': 'bool', 'desc': 'Takes a file path and check if it exist'}]
"

REQUIRED:
I need you to see if there is a coding problem in the query and to solve the coding problem by splitting the task into multiple steps if it needs to and at least 1 step in order to acomplish the required, each step might be a piece of code

Hint:
for each step say brefly what you need to do and which function and how it will be used 


Give the final respond in the form of list with 3 elements 
1) with the step by step solution 
2) with the code that the query asked for
3) All the steps asked for exept for the code it asked for will be stored in second element


"""
# output = generate(query)
# print(output)
# with open("output.txt", "w") as file:
#     file.write(output)