from textnode import TextNode, TextType, extract_markdown_links, extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            split_nodes.append(node)        
        else:
            if delimiter not in node.text:
                split_nodes.append(node)
                continue 
            count = node.text.count(delimiter)
            node_split_on_delim = node.text.split(delimiter)
            if count % 2 != 0:
                raise ValueError(f"Invalid markdown: odd number of delimiters '{delimiter}'")
            for i, text_part in enumerate(node_split_on_delim):
                if text_part == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(text_part, TextType.TEXT))
                else:
                    split_nodes.append(TextNode(text_part, text_type))
    return split_nodes

def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.IMAGE:
            split_nodes.append(node)
        else:
            extracted = extract_markdown_images(node.text)
            if not extracted :
                split_nodes.append(node)
                continue
            current_text = node.text
            for alt, url in extracted:
                string_split = current_text.split(f"![{alt}]({url})", 1)
                if string_split[0] != "":
                    split_nodes.append(TextNode(string_split[0], TextType.TEXT))
                split_nodes.append(TextNode(alt, TextType.IMAGE, url))
                current_text = string_split[1]
            if current_text != "":
                split_nodes.append(TextNode(current_text, TextType.TEXT))
    return split_nodes
            

def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.LINK:
            split_nodes.append(node)
        else:
            extracted = extract_markdown_links(node.text)
            if not extracted :
                split_nodes.append(node)
                continue
            current_text = node.text
            for alt, url in extracted:
                string_split = current_text.split(f"[{alt}]({url})", 1)
                if string_split[0] != "":
                    split_nodes.append(TextNode(string_split[0], TextType.TEXT))
                split_nodes.append(TextNode(alt, TextType.LINK, url))
                current_text = string_split[1]
            if current_text != "":
                split_nodes.append(TextNode(current_text, TextType.TEXT))
    return split_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes