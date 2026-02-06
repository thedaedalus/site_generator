import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://google.com"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://google.com"')

    def test_multiple_props(self):
        props = {"href": "https://google.com", "target": "_blank"}
        node = HTMLNode("a", "link", None, props)
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://google.com" target="_blank"')

    def test_props_none(self):
        node = HTMLNode("a", "link", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("i", "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode(None, "child3")
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<p><i>child1</i><b>child2</b>child3</p>")

    def test_to_html_multiple_children_grandchild(self):
        grandchild_node = LeafNode(None, "grandchild")
        child_node1 = LeafNode("i", "child1")
        child_node2 = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("p", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<p><i>child1</i><div>grandchild</div></p>")

    def test_to_html_with_child_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"href": "https://google.com"})
        self.assertEqual(parent_node.to_html(), '<div href="https://google.com"><span>child</span></div>')


if __name__ == "__main__":
    unittest.main()
