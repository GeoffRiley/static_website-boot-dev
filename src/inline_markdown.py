import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes=None, delimiter=None, text_type=None):
    if delimiter is None or delimiter == "":
        raise ValueError("delimiter must be a non-empty string")

    new_nodes = []
    for node in old_nodes:

        node_type = node.text_type

        if node_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: missing closing delimiter")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^]]+)\]\(([^)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

