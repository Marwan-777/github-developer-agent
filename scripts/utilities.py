import inspect
from typing import get_type_hints
import re
from io import StringIO
import json

def describe_function(func):
    sig = inspect.signature(func)
    hints = get_type_hints(func)
    def type_to_str(t):
        type_map = {
            str: "string",
            int: "integer",
            float: "float",
            bool: "boolean",
            list: "list",
            dict: "dictionary",
            tuple: "tuple",
            set: "set",
            type(None): "null"
        }
        return type_map.get(t, t.__name__ if hasattr(t, "__name__") else str(t))
    attributes = {name:{"type":type_to_str(hints.get(name, 'No type'))} for name in sig.parameters.keys()}

    return attributes, type_to_str(hints.get('return', 'No Type'))

def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses 

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""

def path_list_to_tree(path_list, prefix=""):
    def build_tree(paths):
        """
        Build a nested dictionary representing the directory tree.
        Each directory is a dict; files are represented as empty dicts.
        """
        tree = {}
        for path in paths:
            parts = path.strip("/").split("/")
            node = tree
            for part in parts:
                node = node.setdefault(part, {})
        return tree
    node = build_tree(path_list)
    """
    Recursively build the tree structure as a string.
    """
    output = StringIO()
    
    def _render(node, prefix):
        items = sorted(node.items(), key=lambda x: x[0])
        total = len(items)
        for index, (name, child) in enumerate(items, start=1):
            is_last = (index == total)
            branch = "└── " if is_last else "├── "
            output.write(f"{prefix}{branch}{name}\n")
            if child:
                extension = "    " if is_last else "│   "
                _render(child, prefix + extension)

    _render(node, prefix)
    return output.getvalue()


def get_notebook_content(raw_notebook):
    content = json.loads(raw_notebook)
    new_content = [
        " ---------- Code ----------\n" + "".join(cell["source"])
        if cell["cell_type"] == "code"
        else " ---------- Markdown ----------\n" + "".join(cell["source"])
        for cell in content['cells'] 
        if (cell['cell_type'] == "code" or cell["cell_type"] == "markdown") and cell['source'] 
    ]
    final_content = "\n\n".join(new_content)
    return final_content
