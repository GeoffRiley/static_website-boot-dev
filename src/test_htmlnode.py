import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_p(self):
        node = HTMLNode(tag='p',value="This is some paragraph text")
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, "This is some paragraph text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_a(self):
        node = HTMLNode(tag='a', value="google", props={'href': 'http://www.google.com', 'target': '_blank'})
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'google')
        self.assertIsNone(node.children)
        self.assertEqual(node.props_to_html(), ' href="http://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag='p', value="Yibble ye not!", children=None, props={"id": "robert"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Yibble ye not!, children: None, {'id': 'robert'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_p(self):
        node = LeafNode('p', "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node.tag, 'p')
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode().to_html()

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode().to_html()

    def test_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")


if __name__ == "__main__":
    unittest.main()


