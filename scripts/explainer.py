from openai_llm import generate_stream, generate
from github_interface import get_repo_structure, get_file_content
from pathlib import Path
import json
from utilities import path_list_to_tree, get_notebook_content




summerize_prompt = """
    [Role]
    You are a software enginner who understands code, notebooks and markdown language for readme and mermaid charts

    [Task]
    - Your task is to explain the code given in the input, your answer must be concise and capture keypoints in the code

    [Input]
    - A python script code, notebook with the code and text or a readme file that contains description and charts

    [Output]
    You should give the following:
    1) short text summary explaining what does this script/file do
    2) A string drawing using arrows (-->) to explain the code flow.
        code flow is how user defined ffunctions/classes communicate with each other (if there is no certain flow then leave it empty)
        Note: This step is ONLY for code and NOT for markdown language
    3) Frameworks or modules used: just a list of them

"""
def summarizer():
    # with open("summarizer_output.txt", 'r', encoding="utf-8") as f:
    #     summary_output = f.read()
    #     print(summary_output)
    #     return summary_output
    print("Summerizing ...")
    explaination_files = [file for file in get_repo_structure() if Path(file).suffix in ['.py', '.ipynb','.md'] and "checkpoint" not in file]
    summary = "\n\n ===================================== File structure ===================================== \n\n"
    summary += path_list_to_tree(get_repo_structure())
    for file in explaination_files:
        summary += f"\n\n ===================================== {file} ===================================== \n\n"
        file_content = get_file_content(file)
        file_content = get_notebook_content(file_content) if Path(file).suffix == ".ipynb" else file_content
        messages = []
        messages.append({"role":"system", "content": summerize_prompt})
        messages.append({"role":"user", "content": file_content})

        summary += generate(messages=messages, model="gpt-4.1-mini")
        # for word in generate_stream(messages=messages, model="gpt-4.1-mini"):
        #     print(word, end = "" , flush= True)
        #     summary += word

    with open(f"summarizer_output.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    return summary



print()

explainer_prompt = """
    [Role]
    You are a code explainer who answer questions based on summaries. You should be very friendly and act as a helper.
    [Task]
    - You will be given code or markdown language summary and you are supposed to answer a question regarding it
    - Make the answer short and concise, address the keypoints and keywords and mention important function names from code if needed 
    - You are dealing with software/AI engineers so don't use general terms be technical
    [Input]
    Code or markdown summary and a user query regarding it.
    [Output]
    A Text answering the user query, use emojies

    [Reminder]
    - Make your answer short and address only very important points and keywords 
    - Be very friendly and have a welcoming attitude at the beginning of the answer specially
    - Be helpful in mentioning scripts/functions names if needed
"""
# print(' ------------ Explainer ------------')
# query = "How does it calculate distance and also explain the training process and the data used. mention quickly where can I find the distance calc. part"
# query = "where can I find the distance calculation part."
# query = "what does this repo do in a nutshell and list the frameworks used"
# query = "Explain how the repo works including its file structure, code flow, logic, and frameworks used."
# explain_messages = []
# explain_messages.append({"role":"system", "content": explainer_prompt})
# explain_messages.append({"role":"user", "content": f"[Summary]\n {summary_output} \n\n [query]\n{query}"})
# for word in generate_stream(messages=explain_messages):
#     print(word, end = "" , flush= True)

