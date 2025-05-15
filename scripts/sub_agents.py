from openai_llm import generate, generate_stream
from github_interface import *
from coder import coder
from utilities import extract_xml
from explainer import summarizer

query = """I need to create a function that takes a PIL image and output a PIL image with a horizontal and vertical line in the image in random places name the 
            script img_modification and if it exist replace the old content also add the requirements to the requirements file and create one if not found.
"""
# query = """Create 2 py scripts one (img_download) that takes image url and convert it to PIL type, and the other (img_enhance) will perform 
# enhancement on the image to make it sharper. push the 2 and save their requirements.
# """
#Hint: it can take explainer function output for the repo to build a readme and mermaid file
query = """ I need to modify the code in utilities script to make the function that takes path list and give tree return the string instead of printing it """

def thinker(query):
  system_role = f"""
  [ROLE]:
  You are a software engineer who solves coding problems by breaking them down into step-by-step solution of either manipulating github remote repo
  or creating python code.

  [Task]:
  - Take the query in the input section and break it down into steps to solve the problem step by step, use the provided tools to accomplish the task
  - Write a comprehensive description for the coder to get a code as required in the input by writing every single requirement explicitly.
  - Make the steps in the best order that make it easy for implementation that related steps are sequential.
  - Explain whether an overwrite or concatenatino will be done before writing the steps since it will affect the conditions of read/write to the
    repo
  - Handles file creation, read/write to repo explicitly for each file
  - In case of code modify, You must provide the function with both the old code and the description of modifications
  [Input]:
  You can expect reuqirements for creating code and manipulating github repo files, or even some queries about the repo without code generation.
  code might either be python or markdown.

  Use your intelligence to explain the input user requirements more to be more easly understood and solved

  [Output]:
  You should only and only output :

  1- Your suggestion of step by step solution with numbered points
  2- proposed tools and when to use them

  Make your steps concise and not long for another LLM model to comprehend and implement easily

  Example ouptut:
  ```
  1. **Call the coder function for the first script (img_download)**: 
    - Use the `coder` function with a detailed description that the script `img_download` should take an image URL as input and convert it to a PIL image type. 
    - The description must explicitly mention the usage requirements for PIL library to work with image files.

  2. **Split the output of the coder function for (img_download)**: 
    - Use the `extract_xml` function to get both the code and the requirements for the img_download script.
    - Extract the code using the `<code></code>` tag and the requirements using the `<requirements></requirements>` tag.

  3. **Call the coder function for the second script (img_enhance)**: 
    - Use the `coder` function again with a detailed description that the script `img_enhance` should take an image input (likely a PIL Image object) and perform enhancements to make it sharper.
    - Make sure to include the corresponding requirements that pertain to image enhancement, possibly using the PIL library or any other relevant libraries.

  4. **Split the output of the coder function for (img_enhance)**: 
    - Again, use the `extract_xml` function to get the code and requirements for the img_enhance script, similarly to step 2.

  5. **Check for file existence and handle overwrites**:
    - Check if the files `img_download.py` and `img_enhance.py` already exist in the repo using the `file_exists` function.
    - If they exist, opt to overwrite the files with the new content (if they are being updated).

  6. **Push the image download script (img_download)**:
    - Use the `push_file` function to push the `img_download.py` file along with its content and a relevant commit message to the repository.

  7. **Push the image enhancement script (img_enhance)**:
    - After the first file is pushed, similarly, use the `push_file` function to push the `img_enhance.py` file along with its content and a relevant commit message to the repository.

  8. **Merge requirements**:
    - Before finalizing, check and merge the requirements derived from both scripts into a single requirements file, ensuring there are no redundant entries.

  9. **Push or update requirements**:
      - Given the merged requirements check if requirements.txt file exists concat these new requirements without redundancy if not exist push it.

  **Proposed Tools**:
  - `coder`: To generate the code for both scripts and their requirements.
  - `extract_xml`: To split the generated output into code and requirements for both scripts.
  - `file_exists`: To check if the script files already exist in the repo before pushing.
  - `push_file`: To push both script files to the repository once they are created/updated.
  - 'update_file': To update requirements file if it already exists
  - 'get_file_content': to concat the new dependancies to the old one
  ```

  [Capabilities & constraints]:
  1) You can use these tools to help you in your steps and use only the neccessary:
  {show_capabilities()},
  [
          "type":"function",
          "function":[
              "name":"coder",
              "description": "This function used to write python code and markdown code for README and mermaid chart.
                              - It takes detailed description of the code required
                              - It can take a code and modify it with this format in the input:
                                [Old code]: # old code
                                [Required]: # the required to be modified
                              it always returns 2 tags:
                              <code></code> that holds the code
                              <requirements></requirements> for python code requirements 
                              THE FUNCTION IS CALLED ONCE THEN CODE AND REQUIREMENTS FILE ARE EXTRACTED FROM THE SAME OUTPUT",
              "parameters":[
                  "type": "object",
                  "properties": ["code_desc": ["type":"string"]],
                  "required": ["code_desc"],
              ]
          ]
      ],
      [
          "type":"function",
          "function":[
              "name":"extract_xml",
              "description": "This is a function takes text and return the content of a specified tag in that text and it must be used in case
                              of spliting the code generation ouptut into code and requirements file.",
              "parameters":[
                  "type": "object",
                  "properties": ["text": ["type":"string"], "tag":["type":"string"]],
                  "required": ["text","tag"]
              ]
          ]
      ],
      [
          "type":"function",
          "function":[
              "name":"summarizer",
              "description": "This function is used to explain how the repo code works, 
                              It can be used to explain how the code flow and logic and frameworks used.",
              "parameters":[]
          ]
      ]

  [Reminders]
  - Don't forget to split the coder output into code and requirements file
  - Make sure that the added new requirements to the existing file are not redundant (note: the dependancy might be in the file with specific virsion)
  - You do not create code, you just give steps to solve the problem.
  - You don't suggest dependancies you extract them from the code generation function
  - You do not create code, if you need, you use the coder() function
  - Explicitly distinguish between user requirements and code requirements (dependencies) whenever mentioning "requirements".
  - if mermaid chart is required, its added to the readme file
  - If a readme is needed: summarizer() -> coder(). Use the summarizer output inside the coder input
  - DO NOT add the repo name to the file name 
  """

  print(" =============== Thinker output ===============")
  messages = []
  messages.append({"role":"system", "content": system_role})
  messages.append({"role": "user", "content": query})
  print("Thinking ...")
  instructions = generate(messages, model = "gpt-4.1-mini")
  # instructions = ""
  # for word in generate_stream(messages, model = "gpt-4.1-mini"):
  #       print(word, end = "" , flush= True)
  #       instructions += word
  # print()
  return instructions


reflecting_system_prompt = f"""
  [Role]
  You are an expert senior software engineer who validates if user requirements are met given a proposed solution steps.

  [Task]
  You will be given user requirements and a proposed solution steps and you should evaluate only the following:
  - No retrieval of file content that will not be used
  - Prompt given to code generation function is sufficient and doesn't miss any user requirement
  - DO NOT mention anything related to requirements file in code generation prompt,
  - Make sure that steps are in proper ordering (ex: requirements file and code file are obtained before pushing or updating)


  [Input]
  You will get both user requirements and proposed steps

  [Output]
  Output 2 xml tags:
  <feedback>
    # Here you write the modification to the code that will make the steps acceptable and will be in bullit points (-)
    # Do NOT mention points that are not quite right about the steps (be 100% sure)
    # Mention the supporting rule for each point
  </feedback>

  <status>
    # Here you will only either write "PASS" or "FAIL" depending on the criteria
    status is PASS if there are only 2 or 3 negative feedbacks (that might be niglected)
  </status>



  [Capabilities]
  Given these capabilities to konw the use of each function:
    {tools}
  [Reminders]
  - Do not mention any files related commands in the code generation prompt 
  - One code generation per script

  """

# reflecting_messages = []
# reflecting_messages.append({"role":"system", "content": reflecting_system_prompt})
# reflecting_messages.append({"role":"user", "content": ""})
# print(" ---------- Reflecting ----------")
# for i in range(3):

#   reflecting_messages[-1]["content"] = f"""
#     [User requirements]
#     {query}

#     [Proposed steps]
#     {instructions}
#     """
#   reflections = ""
#   for word in generate_stream(reflecting_messages):
#       print(word, end = "" , flush= True)
#       reflections += word
#   if "FAIL" in extract_xml(reflections, "status"):
#       print(" ---------- Fail ----------")
#       feedback = extract_xml(reflections, "feedback")
#       messages.append({"role":"assistant", "content": instructions})
#       messages.append({"role": "user", "content": f"""[Feedback]: \n {feedback}"""})
      
#   else:
#       print(" ---------- ",extract_xml(reflections,"status"), " ----------")
#       break
  
#   instructions = "" 
#   for word in generate_stream(messages):
#       print(word, end = "" , flush= True)
#       instructions += word


# ======================================= Executer =======================================
def executer(instructions):
  executor_prompt = f"""
  [Role]:
  You are a software engineer who uses a coder function that create scripts and you can use github to manipulate files in the remote repo

  [Task]
  - You will be given a set of steps and you should give e python code that implements these steps as mentioned
  - Be smart on writing your code that you could blend things and minimize redundancy to give more optimized code with 
  correct logic that reflect the ouptut intended from the Input instructions.
  - If multiple py scripts are created, concatinate all the requirements files into one file.

  [Input]:
  You will be given a set of instructions and proposed tools to use to solve the problem.

  [Output]:
  The output should be 1 xml tag:

  <flow_code>
  # python code that implement the steps flow. 
  </flow_code>

  Note: Functions calling MUST be as follows:
    function_name(arg_name = "arg_value")
  #DO NOT give the function a dictionary of args

  [Capabilities & constraints]:
  1) You can use these tools to help you in your steps and use only the neccessary:
  {show_capabilities()},
  [
      "type":"function",
      "function":[
          "name":"coder",
          "description": "This function used to write python code and markdown code for README and mermaid chart.
                              - It takes detailed description of the code required
                              - It can take a code and modify it with this format in the input:
                                [Old code]: # old code
                                [Required]: # the required to be modified
                              it returns 2 tags:
                              <code></code> that holds the code
                              <requirements></requirements> for python code requirements 
                              THE FUNCTION IS CALLED ONCE THEN CODE AND REQUIREMENTS FILE ARE EXTRACTED FROM THE SAME OUTPUT",
          "parameters":[
              "type": "object",
              "properties": ["code_desc": ["type":"string"]],
              "required": ["code_desc"],
          ]
      ]
  ],
  [
      "type":"function",
      "function":[
          "name":"extract_xml",
          "description": "This is a function takes text and return the content of a specified tag in that text and it must be used in case
                          of spliting the code generation ouptut into code and requirements file.",
          "parameters":[
              "type": "object",
              "properties": ["text": ["type":"string"], "tag":["type":"string"]],
              "required": ["text","tag"]
          ]
      ]
  ],
  [
          "type":"function",
          "function":[
              "name":"summarizer",
              "description": "This function is used to explain how the repo code works, 
                              It can be used to explain how the code flow and logic and frameworks used.",
              "parameters":[]
          ]
      ]
  ]


  [Reminders & contraints]:
  1) Don't provide your opinion or any other text other than the instructions flow implimentation code
  2) You can use the functions names mentioned right away that is mentioned in the tool name.

  """


  print(" ==================== Executor output ====================")
  execution_code = ""
  executor_messages = []
  executor_messages.append({"role":"system", "content": executor_prompt})
  executor_messages.append({"role": "user", "content": instructions})
  print("Executing ...")
  execution_code = generate(executor_messages, model="gpt-4.1-mini")
  # for word in generate_stream(executor_messages, model="gpt-4.1-mini"):
  #     print(word, end = "" , flush= True)
  #     execution_code += word
  return execution_code

# with open("Instructions_execution.py", "w") as f:
#     f.write(extract_xml(execution_code, "flow_code"))

def developer(query):
    instructions = thinker(query)
    executable_instructions = extract_xml(executer(instructions), "flow_code")
    exec(executable_instructions)
    return "Done"
# developer(query)
