from github import Github
from github import Auth
from utilities import describe_function
from dotenv import load_dotenv
import os
load_dotenv() 


auth = Auth.Token( os.getenv("github_key"))
g = Github(auth=auth)
user = g.get_user()
repo_name = "lab-agile-planning"
repo = user.get_repo(repo_name)

def get_repo_name():
    return repo_name
def set_repo_name(name):
    try:
        global repo, repo_name
        repo_name = name
        repo = user.get_repo(repo_name)
    except Exception as e:
        print("Error occured: ", e)
def list_repos():
    return [repo.name for repo in user.get_repos()]

def show_admin_methods():
    methods = [
        {
            "type":"function",
            "function":{
                "name":"get_repo_name",
                "description": "It gets the current working github repository name",
                "parameters":{}
            }
        },
        {
            "type":"function",
            "function":{
                "name":"set_repo_name",
                "description": "It changes the name of the current working github repository",
                "parameters":{
                    "type": "object",
                    "properties": describe_function(set_repo_name)[0],
                    "required": list(describe_function(set_repo_name)[0].keys()),
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"list_repos",
                "description": "List all the repository names the user have",
                "parameters":{}
            }
        },
        {
            "type":"function",
            "function":{
                "name":"get_repo_structure",
                "description": "It returns the file structure of the repo",
                "parameters":{}
            }
        }

    ]
    return methods
def show_capabilities():
    tools = [
        {
            "type":"function",
            "function":{
                "name":"push_file",
                "description": "It pushes a new file to the repo if it doesn't exist",
                "parameters":{
                    "type": "object",
                    "properties": describe_function(push_file)[0],
                    "required": list(describe_function(push_file)[0].keys()),
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"update_file",
                "description": "It updates an existing file with new content",
                "parameters":{
                    "type": "object",
                    "properties": describe_function(update_file)[0],
                    "required": list(describe_function(update_file)[0].keys()),
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"get_file_content",
                "description": "Takes a file path gets its content in case it will be modified \
                            (This function is not needed if the content will be replaced).",
                "parameters":{
                    "type": "object",
                    "properties": describe_function(get_file_content)[0],
                    "required": list(describe_function(get_file_content)[0].keys()),
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"file_exists",
                "description": "Takes a file path and check if it exist",
                "parameters":{
                    "type": "object",
                    "properties": describe_function(file_exists)[0],
                    "required": list(describe_function(file_exists)[0].keys()),
                }
            }
        }
    ]
    return tools



def push_file(file_path: str, file_content :str, commit_msg :str= "Commit from agent M"):

    try:
        repo.create_file(
            path=file_path,       # Folder and file path in repo
            message=commit_msg,          # Commit message
            content=file_content,              # File content
            branch="main"                      # Target branch
        )
        print('Successfull push')
    except Exception as e:
        print('Pushing Faild', e)

def update_file(file_path: str, new_content: str):
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(
            path = contents.path, 
            message = commit_msg, 
            content = new_content, 
            sha = contents.sha)
        print("File updated")
    except Exception as e:
        print("File update failed")

def get_file_content(file_path: str) -> str:
    file = repo.get_contents(file_path)
    return file.decoded_content.decode("utf-8")

def file_exists(file_path: str) -> bool:
    try:
        file = repo.get_contents(file_path)
        return True
    except Exception as e:
        return False

def get_repo_structure() -> list:
    file_tree = repo.get_git_tree("HEAD", recursive=True).tree
    return [i.path for i in file_tree if i.type == "blob"]


# *********************************** Testing ***********************************

tools = [
    {
        "type":"function",
        "function":{
            "name":"push_file",
            "description": "It pushes a new file to the repo if it doesn't exist",
            "parameters":{
                "type": "object",
                "properties": describe_function(push_file)[0],
                "required": list(describe_function(push_file)[0].keys()),
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"update_file",
            "description": "It updates an existing file with new content",
            "parameters":{
                "type": "object",
                "properties": describe_function(update_file)[0],
                "required": list(describe_function(update_file)[0].keys()),
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_file_content",
            "description": "Takes a file path gets its content in case it will be modified \
                        (This function is not needed if the content will be replaced).",
            "parameters":{
                "type": "object",
                "properties": describe_function(get_file_content)[0],
                "required": list(describe_function(get_file_content)[0].keys()),
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"file_exists",
            "description": "Takes a file path and check if it exist",
            "parameters":{
                "type": "object",
                "properties": describe_function(file_exists)[0],
                "required": list(describe_function(file_exists)[0].keys()),
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"coder",
            "description": """This is a function (sub-agent) that takes a detailed code description that need to be implemented and  write code 
                            whether python or markdown and it returns 2 tags:
                            <code></code> that holds the code
                            <requirements></requirements> for python code requirements 
                            The function is called once then code and rquirements are extracted from the same ouptut""",
            "parameters":{
                "type": "object",
                "properties": {"code_desc": {"type":"string"}},
                "required": ["code_desc"],
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"extract_xml",
            "description": "This is a function takes text and return the content of a specified tag in that text.",
            "parameters":{
                "type": "object",
                "properties": {"text": {"type":"string"}, "tag":{"type":"string"}},
                "required": ["text","tag"]
            }
        }
    }
]
# print(tools)

# print(show_capabilities())


file_path = "README.md"
new_function_code = """
This is the readme updated by the github interface from my code :)

"""
commit_msg = "pushed by AI"

# if file_exists(file_path):
#     existing_content = get_file_content(file_path)
#     updated_content = existing_content.strip() + "\n\n" + new_function_code.strip()
#     update_file(file_path, updated_content)
# else:
#     # Step 4: Create new file with the function
#     push_file(file_path, new_function_code.strip(), commit_msg)


g.close()