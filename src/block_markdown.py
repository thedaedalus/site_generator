import re
import textwrap
from enum import Enum

import htmlnode
import inline_markdown as im
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def text_to_children(text):
    text_nodes = im.text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def block_heading_type(heading):
    parts = []
    if heading.startswith("# "):
        parts = heading.split("# ", maxsplit=1)
        return ParentNode("h1", children=text_to_children(parts[1]))
    elif heading.startswith("## "):
        parts = heading.split("## ", maxsplit=1)
        return ParentNode("h2", children=text_to_children(parts[1]))
    elif heading.startswith("### "):
        parts = heading.split("### ", maxsplit=1)
        return ParentNode("h3", children=text_to_children(parts[1]))
    elif heading.startswith("#### "):
        parts = heading.split("#### ", maxsplit=1)
        return ParentNode("h4", children=text_to_children(parts[1]))
    elif heading.startswith("##### "):
        parts = heading.split("##### ", maxsplit=1)
        return ParentNode("h5", children=text_to_children(parts[1]))
    elif heading.startswith("###### "):
        parts = heading.split("###### ", maxsplit=1)
        return ParentNode("h6", children=text_to_children(parts[1]))
    else:
        raise ValueError("This is not a heading block")


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def code_block(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_block(quote):
    quote_elements = quote.split("\n")
    quote_list = []
    for quote in quote_elements:
        if not quote.startswith(">"):
            raise ValueError("invalid quote block")
        quote_list.append(quote.lstrip(">").strip())
    content = " ".join(quote_list)
    children = text_to_children(content)
    block_quote = ParentNode("blockquote", children)
    return block_quote


def list_lines(lines):
    line_sections = []
    for line in lines:
        if line == "":
            continue
            line = line.strip("\n")
        line_sections.append(ParentNode("li", text_to_children(line)))
        # print(line_sections)
    return line_sections


def ulist_block(ulist):
    lines = ulist.splitlines()
    cleaned_list = [line.lstrip("- ").strip() for line in lines]
    sections = []
    sections.extend(list_lines(cleaned_list))
    return ParentNode("ul", sections)


def olist_block(olist):
    lines = olist.splitlines()
    cleaned_list = [re.sub(r"\d. ", "", item) for item in lines if item]
    sections = []
    sections.extend(list_lines(cleaned_list))
    return ParentNode("ol", sections)


def markdown_to_html_node(markdown):
    sections = []
    blocks = markdown_to_blocks(markdown)
    blocks = [re.sub(r"\n\s+", "\n", item) for item in blocks if item]
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                parent = block_heading_type(block)
            case BlockType.PARAGRAPH:
                parent = paragraph_to_html_node(block)
            case BlockType.CODE:
                parent = code_block(block)
            case BlockType.QUOTE:
                parent = quote_block(block)
            case BlockType.ULIST:
                parent = ulist_block(block)
            case BlockType.OLIST:
                parent = olist_block(block)
            case _:
                raise ValueError("ERROR: block type is not a valid HTML block")
        sections.append(parent)
    return ParentNode("div", sections)


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


if __name__ == "__main__":
    pass
