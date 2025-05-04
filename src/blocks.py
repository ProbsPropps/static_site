from enum import Enum
import re
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from splitnodes import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = re.split("\ns*\n", markdown)
    proper_split = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            normalized = re.sub(r"\n\s+", "\n", stripped)
            proper_split.append(normalized)
    return proper_split

def block_to_block_type(markdown):

    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    
    if re.match(r"^```", markdown) and re.search(r"```$", markdown):
        return BlockType.CODE
    
    lines = markdown.split("\n") if "\n" in markdown else [markdown]

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    is_ordered_list = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
        

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                paragraph_text = block.replace("\n", " ")
                parent_node = ParentNode("p", text_to_children(paragraph_text))
                html_nodes.append(parent_node)
            case BlockType.HEADING:
                start = re.match(r"^(#+)\s+(.+)", block)
                if start:
                    hashes = start.group(1)
                else:
                    raise Exception("Somehow the HEADING BlockType was true without any leading #'s")
                parent_node = ParentNode(f"h{len(hashes)}", text_to_children(start.group(2)))
                html_nodes.append(parent_node)
            case BlockType.UNORDERED_LIST:
                list_lines = []
                if "\n" in block:
                    lines = block.split("\n")
                else: lines = [block]
                for line in lines:
                    if not line.strip(): continue
                    split = re.match(r"^\s*[*\-+]\s+(.*)", line)
                    if split:
                        just_text = split.group(1).strip()
                        list_lines.append(ParentNode("li", text_to_children(just_text)))
                parent_node = ParentNode("ul", list_lines)
                html_nodes.append(parent_node)
            case BlockType.ORDERED_LIST:
                list_lines = []
                if "\n" in block:
                    lines = block.split("\n")
                else: lines = [block]
                current_num = 1
                for line in lines:
                    if not line.strip(): continue
                    split = re.match(r"^(\d+)\.\s+(.*)", line)
                    if split:
                        just_text = split.group(2).strip()
                        if current_num == int(split.group(1)):
                            list_lines.append(ParentNode("li", text_to_children(just_text)))
                            current_num += 1
                        else:
                            raise Exception("Looks like you don't have a correct sequence of numbers for your ordered list")
                parent_node = ParentNode("ol", list_lines)
                html_nodes.append(parent_node)
            case BlockType.QUOTE:
                list_lines = []
                if "\n" in block:
                    lines = block.split("\n")
                else: lines = [block]
                for line in lines:
                    if not line.strip(): continue
                    split = re.match(r"^\>+\s+(.*)", line)
                    if split:
                        just_text = split.group(1).strip()
                        list_lines.extend(text_to_children(just_text))
                parent_node = ParentNode("blockquote", list_lines)
                html_nodes.append(parent_node)
            case BlockType.CODE:
                lines = block.split("\n")
                if lines[-1].strip() == "```":
                    just_text = just_text = "\n".join(lines[1:-1]) + "\n"
                else:
                    just_text = just_text = "\n".join(lines[1:-1])
                code_node = LeafNode("code", just_text)
                outer_parent = ParentNode("pre", [code_node])
                html_nodes.append(outer_parent)
    return ParentNode("div", html_nodes)

                


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children
            