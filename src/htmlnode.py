class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_string = ""
        if self.props is None:
            return ""

        for key, value in list(self.props.items()):
            html_string += f' {key}="{value}"'
        return html_string

    def __repr__(self):
        return f"HtmlNode({self.tag},{self.value},{self.children},{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("ERROR: No Value Provided")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HtmlNode({self.tag},{self.value},{self.props}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # tag and children are required, value is always None for ParentNode
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        # Build the HTML for all children by calling their own to_html()
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        # Use the same props-to-HTML helper as LeafNode/HTMLNode
        props_html = self.props_to_html() if self.props else ""

        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
