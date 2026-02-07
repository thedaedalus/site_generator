import re
from logging import ERROR

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes is None:
        raise ValueError("ERROR: no nodes where provided")
    new_nodes = []
    new_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("ERROR: Invalid markdown section was not closed")

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                section = TextNode(split_text[i], TextType.TEXT)
                new_node.append(section)
            else:
                section = TextNode(split_text[i], text_type)
                new_node.append(section)

        new_nodes.extend(new_node)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    if old_nodes is None:
        raise ValueError("ERROR: no nodes where provided")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        matches = extract_markdown_images(original_text)
        new_node = []
        running = True

        while running:
            matches = extract_markdown_images(original_text)
            if not matches:
                running = False
                break
            image_alt, image_link = matches[0]
            image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            new_node.append(TextNode(sections[0], TextType.TEXT))
            new_node.append(image_node)
            original_text = sections[1]

        new_nodes.extend(new_node)
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    if old_nodes is None:
        raise ValueError("ERROR: no nodes where provided")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        matches = extract_markdown_links(original_text)
        new_node = []
        running = True

        while running:
            matches = extract_markdown_links(original_text)
            if not matches:
                running = False
                break
            link_text, link = matches[0]
            image_node = TextNode(link_text, TextType.LINK, link)
            sections = original_text.split(f"[{link_text}]({link})", 1)
            new_node.append(TextNode(sections[0], TextType.TEXT))
            new_node.append(image_node)
            original_text = sections[1]

        new_nodes.extend(new_node)
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


if __name__ == "__main__":
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes)
    matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
    # print(matches)
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_links([node])
    print(new_nodes)
