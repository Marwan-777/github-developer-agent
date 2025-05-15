from utilities import extract_xml
from openai_llm import generate_stream, generate
from explainer import summarizer
# Used to create the file structure string
code_desc = """given the tree of files paths in repo:
README.md
final_scirpt
my_script.py
test_folder/my_script.py

write a python code to get the text representation like you do, the code should take a list of paths and ouptut the text structure.
"""

code_desc = """

Create a README file for the repo with this description:

Hello! 😊 I'm excited to help you understand how this Uber fare prediction repository works!

### File Structure:
- **.ipynb_checkpoints/**: Contains Jupyter Notebook checkpoints.
- **README.md**: Contains project overview and usage instructions.
- **development/**: 
  - **NYC Uber fare EDA and Model Training.ipynb**: Main script for model development, including data preprocessing and training.
  - **mlflow.db**: Database for tracking experiments with MLflow.
  - **models/**: Contains saved machine learning models (`xgb_r.bin`, `xgb_r_tuned.bin`).
- **production/**: 
  - Various scripts for testing and deploying the prediction API.
  - **Dockerfile**: For creating a docker image.
  - **prediction_API_script.py**: Hosts the Flask API for fare prediction.

### Code Flow:
1. **Data Loading & Preprocessing** (in `development/NYC Uber fare EDA and Model Training.ipynb`):
   - Load data, clean it, and engineer features like Haversine distance and cyclical time encoding.
   - Train an XGBoost model (`XGBRegressor`) with hyperparameter tuning tracked via MLflow.

2. **Prediction API** (in `production/prediction_API_script.py`):
   - Reads incoming JSON data.
   - Processes it (calculates features) and utilizes the trained model to predict fares.
   - Flask handles the endpoint at `/predict`.

3. **API Testing**:
   - Scripts like `API_cloud_test.ipynb` and `API_local_test.py` check the API responses by sending requests with testing data.

### Frameworks Used:
- **Python**: Main programming language.
- **Flask**: For creating the prediction API.
- **MLflow**: Tracking models and experiments.
- **Docker**: For containerizing the application ensuring consistent environments.
- **GCP Cloud Run**: For deploying the API service.

This repository showcases a complete cycle from data analysis, model training, to deploying a prediction service. If you have more questions, feel free to ask! 🚀
"""

# code_desc = """
#     def build_tree(paths):
#     tree = {}
#     for path in paths:
#         parts = path.strip("/").split("/")
#         node = tree
#         for part in parts:
#             node = node.setdefault(part, {})
#     return tree

# def print_tree(node, prefix=""):
#     # Sort keys to have deterministic order: directories and files mixed alphabetically
#     items = sorted(node.items(), key=lambda x: x[0])
#     total = len(items)
#     for index, (name, child) in enumerate(items, start=1):
#         is_last = (index == total)
#         # Choose branch character
#         branch = "└── " if is_last else "├── "
#         print(f"{prefix}{branch}{name}")
#         # If this node has children (i.e., it's a directory), recurse
#         if child:
#             # Extend prefix: if last, add spaces; otherwise, add a vertical line
#             extension = "    " if is_last else "│   "
#             print_tree(child, prefix + extension)
# """

def coder(code_desc):
    coder_prompt = f"""
        [Role]:
        You are a professional coder who can create/modify python scripts, README files and mermaid charts and more.

        [Task]:
        - Given the code description in the input, you should create a code that perform the task required.
        - The user can give you a code and ask for modifications on this code
        - In case of README file: DO NOT make things up and don't write the file structure, give a good explaination of how the repo works

        [Input]:
        - A code description for either python or markdown for README or mermaid chart
        - The user can give you a code to modify

        [Output]:
        You will output 2 xml tags:

        <code>
        # Here is the code script (whether python or markdown or mermaid flowchart code)
        </code>

        <requirements>
            # Make sure to list the required modules to run the code
            # if code is not python code this tag should be empty.
        </requirements>
        
        
        [Constraints]:
        - Make your code comprehensive and efficient
        - Add comments for python code only, and do not add comment for markup code
        - Enhance your thought process before coding to get the best code possible
        """

    # final_query = f"[Old code]\n{code_desc} \n\n [Required]\n I need this code to  save the printed string in str var and return it instead of printing it and if there is more efficient way to do it"
    messages = []
    messages.append({"role":"system", "content": coder_prompt})
    messages.append({"role":"user", "content":code_desc})
    print("Coding ...")
    coder_output = generate(messages=messages, model="o4-mini")
    return coder_output

# coder(code_desc)