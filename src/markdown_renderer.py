from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes is None:
        raise ValueError("ERROR: no nodes where provided")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("ERROR: Invalid markdown section was not closed")

        new_node = []
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
