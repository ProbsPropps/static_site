from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        #Checking if the other object is a TextNode object
        if not isinstance(other, TextNode):
            return False
        
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    
    def __repr__(self):
        if self.url is not None:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type.value}, None)"
    
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.TEXT):
            return LeafNode(tag=None,value=text_node.text)
        case(TextType.BOLD):
            return LeafNode(tag="b", value=text_node.text)
        case(TextType.ITALIC):
            return LeafNode(tag="i", value=text_node.text)
        case(TextType.CODE):
            return LeafNode(tag="code", value=text_node.text)
        case(TextType.LINK):
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case(TextType.IMAGE):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Current text type is not valid")
        
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

