import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a url node", TextType.LINK, url="https://google.com")
        self.assertTrue(
            node.url is not None,
        )

    def test_url_none(self):
        node = TextNode("This is an image", TextType.IMAGE)
        self.assertTrue(
            node.url is None,
        )


if __name__ == "__main__":
    unittest.main()
