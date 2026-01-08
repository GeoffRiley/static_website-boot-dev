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

def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        image_nodes = extract_markdown_images(old_node.text)
        if not image_nodes:
            node_list.append(old_node)
            continue

        current_text = old_node.text
        for img_alt, img_link in image_nodes:
            pattern = f"![{img_alt}]({img_link})"
            before, after = current_text.split(pattern, 1)
            if before != "":
                node_list.append(TextNode(text=before, text_type=TextType.TEXT))
            node_list.append(
                TextNode(text=img_alt, text_type=TextType.IMAGE, url=img_link)
            )
            current_text = after

        if current_text != "":
            node_list.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return node_list


def split_nodes_link(old_nodes):
    node_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        link_nodes = extract_markdown_links(old_node.text)
        if not link_nodes:
            node_list.append(old_node)
            continue

        current_text = old_node.text
        for link_text, link_url in link_nodes:
            pattern = f"[{link_text}]({link_url})"
            before, after = current_text.split(pattern, 1)
            if before != "":
                node_list.append(TextNode(text=before, text_type=TextType.TEXT))
            node_list.append(
                TextNode(text=link_text, text_type=TextType.LINK, url=link_url)
            )
            current_text = after

        if current_text != "":
            node_list.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return node_list

def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
