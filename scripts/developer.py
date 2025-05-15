
from openai_llm import generate, generate_stream
from  github_interface import *
from sub_agents import developer
from explainer import summarizer

'''
    future to-do:
        - try creating and modifying multiple files 
        - handle repo creation

'''


prompt = """
        [Role]
        You are a chatbot that chat with the user without saying lots of things just answer the user with friendly way with short answers
        you should ask any question to clarify the task before answering
        [Task]
        - You will chat with a software/AI enginner who needs to perform some tasks on github
        - You can only do one of the three at a time:
            1) Use a function
            2) Ask a question
            3) Answer the user question (you might use another agent's input for help)
        - After understanding the task You either answer his questions or perform the task required using other helping sub-agents
        - If there is an action required DO NOT chat or say anything, FUNCTION CALL ONLY
        - YOU MUST ALWAYS use the agent answer in the input to clarify to the user.
        
        [Input]
        You can get one of the following:
        - Text message of either a query (question to answer) or a task (problem to solve) from the user
        - An answer from another agent that will help you answer the question (if its empty then its Done successfuly.)

        [Output]
            Your answer MUST BE in either one of the 2 tags only.
            You should always output one of the 2 tags in this EXACT format:

            1- <answer>
            You answer his questions and let other agents do the task required (with no tag footer)
            # DO NOT ANSWER LEAVE IT EMPTY if there is a function call

            2- <function_call>
            # Simple python code to use the function (either update or print a value)

            Example (in case of function call):
            <function_call>
            [
                {
                    "tool": "function_name",
                    "args": {"arg1":"value1"}
                }
            ]
        """ + f"""
            Example (in case of only answering):
            <answer>
            # Question answer in text
            # The clarifying question to ask


        [Capabilities]
        Given this adminstration capabilities:
        {show_admin_methods()}
        [Reminder]
        - Be very friendly and have a welcoming attitude in your chat, Use different emojies
        - DO NOT go to a repo before making sure it exists
        - Search the most suitable repo name before switching to it
        - always give a respond (either function call, question or an answer)
    """

prompt = """
        [Role]
        You are a chatbot that chat with the software/AI enginner who needs to perform some tasks on github without saying lots of things.
        you talk in a friendly and welcoming way. Expect the user to ask questions or give clarifications for you to better understand

        [Task]
        - You can only do one of the three at a time:
            1) function call
            2) Ask a clarification question
            3) Answer the user question (you might use another agent's input for help)

        - After understanding the task You either answer his questions or perform the task required using function call
        - If you have [answer from another agent] in the input you MUST use it to clarify to the user or tell him the what is the error.
        - Tasks you can propagate to another agents are :
            - create/modify python code
            - create/modify readme flie and mermaid chart 
            - push and update the github repo
        - You can use the tools for clarification
        [Input]
        You can get one of the following:
        - A user query (question to answer) or a task (problem to solve) from the user
        - An answer from another agent that will help you answer the question (if its empty then its Done successfuly.)

        [Output]
            Your answer MUST BE either the text and xml tag for the function call. Like this EXACT format:

            1- It might be:
            - Answer to the user question
            - Clarifying question
            - Confirmation to the user 

            

            2- <function_call></function_call>
            contains specs of the function should be used to better answer the question.
            # Only contain this tag if there is a function call else DO NOT include it.

            Example (in case of function call):
            <function_call>
            [
                {
                    "tool": "function_name",
                    "args": {"arg1":"value1"}
                }
            ]
            </function_call>

        """ + f"""
          
        [Capabilities]
        Given this adminstration capabilities:
        {show_admin_methods()}.
        """+ """
        {
            "type":"function",
            "function":{
                "name":"developer",
                "description": "This function is responsible for any action regarding repo manipulation or coding
                                Avery detail explicit description of the requirements and the query should be provided",
                "parameters":{
                    "type": "object",
                    "properties": ["query": ["type":"string"]],
                    "required": ["query"]
                }
            }
        }
        [
                "type":"function",
                "function":[
                    "name":"summarizer",
                    "description": "This function is used to explain how the repo code works, 
                                    It can be used to explain how the code flow and logic and frameworks used.
                                    It DO NOT take any argument",
                    "parameters":[]
                ]
            ]
        ]


        [Reminder]
        - Be very friendly and have a welcoming attitude in your chat, Use different emojies
        - DO NOT go to a repo before making sure it exists
        - Search the most suitable repo name before switching to it
        - always give a respond do not stay silent.
        - DO NOT include the repo name in the file names.
        - When user ask for explaination or summary USE summarizer function and NOT developer and be specific in your explaination
        - If the tool give error, stop trying
    """

chat_history = []
chat_history.append({"role":"system", "content":prompt})



def agent_repond():
    capturing_action = False
    action_code = None
    response = ""
    buffer = ""
    while True:
        for word in generate_stream(chat_history, model="gpt-4.1-mini"):
            buffer += word

            # Switch to action if [Action] appears
            if "<function_call>" in buffer:
                capturing_action = True
                action_code = ""
                buffer = "" if word in [">","\n"] else word
                continue

            if "</function_call>" in buffer:
                action_code = action_code.split("</function", 1)[0]
                capturing_action = False

            if capturing_action:
                action_code += word
            else:
                print(word, end="", flush=True)
                response += word
        

        if action_code:
            function_result = None
            for tool in eval(action_code):
                try:
                    function_result = {tool["tool"]: globals()[tool["tool"]](**tool["args"]) }
                except Exception as e:
                    print("Error in using a tool: ", e)
            chat_history.append({"role":"user", "content": f"[Supporting results from another agent: ]\n{function_result}"})
            print()
            capturing_action = False
            action_code = None
            response = ""
            buffer = ""
        else:
            chat_history.append({"role":"assistant", "content":response})        
            break



messages_count = 0
while True:
    query = input("You: ")
    chat_history.append({"role":"user", "content":query})
    
    print("\nGitHub Agent: ", end = "")
    # response = ""
    # for word in generate_stream(chat_history, model="gpt-4.1-mini"):
    #     print(word, end="", flush=True)
    #     response += word
    # chat_history.append({"role":"assistant", "content": response})
    response = agent_repond()

    if messages_count > 50:
        chat_history = [chat_history[0]].extend(chat_history[3:])
    print("\n")
