import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a HtmlNode", ["a"], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "this is a HtmlNode", ["a"], {"href": "https://www.google.com"})
        node3 = HTMLNode("p")
        node4 = HTMLNode(value="this is a HtmlNode")
        node5 = HTMLNode(children=[node4, node3])
        node6 = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node, node6)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("p", "Hello, world!", {"href": "https://www.amazon.com"})
        self.assertEqual(node2.to_html(), "<p href=\"https://www.amazon.com\">Hello, world!</p>")

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

if __name__ == "__main__":
    unittest.main()