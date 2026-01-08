import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    str_list = []

    temp_list = markdown.split("\n\n")
    for item in temp_list:
        new_item = item.strip()
        if new_item != "":
            str_list.append(new_item)

    return str_list


def is_unordered_list(lines):
    for line in lines:
        if not line.startswith("- "):
            return False
    return True


def is_ordered_list(lines):
    for index, line in enumerate(lines):
        expected_prefix = f"{index + 1}. "
        if not line.startswith(expected_prefix):
            return False
    return True


def block_to_block_type(md_txt_block):
    md_txt_block = md_txt_block.strip()
    lines = md_txt_block.split("\n")
    first_line = lines[0]
    last_line = lines[-1]

    if first_line.startswith("```") and last_line.startswith("```"):
        return BlockType.CODE

    if first_line.startswith("#"):
        heading_counter = 0
        for char in first_line:
            if char == "#":
                heading_counter += 1
            else:
                break
        return BlockType.HEADING

    if first_line.startswith(">"):
        return BlockType.QUOTE

    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def convert_line_type_to_html_tag(line_type, line=None):
    match line_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            if line is not None:
                heading_counter = 0
                for char in line:
                    if char == "#":
                        heading_counter += 1
                    else:
                        break
                return f"h{heading_counter}"
            else:
                raise TypeError("Invalid line value parameter")
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise Exception("Invalid line type")


def handle_clean_line(line_type, line):
    if line_type == BlockType.HEADING:
        return line.lstrip("#").strip()
    elif line_type == BlockType.QUOTE:
        return line.lstrip(">").strip()
    elif line_type == BlockType.CODE:
        result = line.strip()
        if result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        return result.strip() + "\n"
    elif line_type == BlockType.PARAGRAPH:
        return line.replace("\n", " ")
    else:
        return line


def clean_inner_line(inner_line):
    line = inner_line.lstrip()  # bỏ space thừa bên trái cho chắc

    if line.startswith("- ") or line.startswith("* "):
        return line[2:].strip()

    # xử lý dạng "1. text", "2. text"
    match = re.match(r"^\d+\.\s*(.*)$", line)
    if match:
        return match.group(1).strip()

    # nếu không khớp gì, trả lại như cũ
    return line.strip()


def markdown_to_html_node(md):
    lines = markdown_to_blocks(md)
    html_nodes = []

    for line in lines:
        line_type = block_to_block_type(line)
        html_type = convert_line_type_to_html_tag(line_type, line)
        clean_line = handle_clean_line(line_type, line)

        if line_type == BlockType.CODE:
            text_node = TextNode(clean_line, TextType.TEXT)
            code_html = text_node_to_html_node(text_node)

            code_node = ParentNode(tag="code", children=[code_html])

            parent_node = ParentNode(tag=html_type, children=[code_node])
            html_nodes.append(parent_node)
        elif (
            line_type == BlockType.UNORDERED_LIST or line_type == BlockType.ORDERED_LIST
        ):
            inner_lines = line.splitlines()
            li_nodes = []

            for inner_line in inner_lines:
                cleaned_inner_line = clean_inner_line(inner_line)
                text_node_list = text_to_textnodes(cleaned_inner_line)
                children = []

                for text_node in text_node_list:
                    html_node = text_node_to_html_node(text_node)
                    children.append(html_node)

                li_node = ParentNode(tag="li", children=children)
                li_nodes.append(li_node)

            parent_node = ParentNode(tag=html_type, children=li_nodes)
            html_nodes.append(parent_node)
        else:
            text_node_list = text_to_textnodes(clean_line)
            children = []

            for text_node in text_node_list:
                html_node = text_node_to_html_node(text_node)
                children.append(html_node)

            parent_node = ParentNode(tag=html_type, children=children)
            html_nodes.append(parent_node)

    return ParentNode(tag="div", children=html_nodes)


