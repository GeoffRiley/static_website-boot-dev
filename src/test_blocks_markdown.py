import unittest
from textwrap import dedent
from blocks_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """)

        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_with_header(self):
        md = dedent("""
            # This is a heading

            This is a paragraph of text.
            It has some **bold** and _italic_ words inside of it.

            - This is the first list item in a list block
            - This is a list item
            - This is another list item
        """)

        blocks = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text.\nIt has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertEqual(blocks, expected)

    def test_is_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_is_not_code_block(self):
        block = "Hello World!"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_is_heading_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_is_heading_3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_is_not_heading(self):
        block = "Heading 1"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_is_quote_block(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_is_not_quote_block(self):
        block = "This is a quote"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_is_unordered_list(self):
        block = dedent("""
            - This is the first list item in a list block
            - This is a list item
            - This is another list item
        """)
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_is_not_unordered_list(self):
        block = dedent("""
            - This is the first list item in a list block
            This is a list item
            - This is another list item
        """)
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_is_ordered_list(self):
        block = dedent("""
            1. first
            2. second
            3. third
        """)
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_is_not_ordered_list(self):
        block = dedent("""
            1. first
            3. third
        """)
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_is_paragraph(self):
        block = "Hello World!"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownHeaderBlocks(unittest.TestCase):
    def test_header_h1(self):
        md = dedent("""
            # H1 Header
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1 Header</h1></div>"
        )

    def test_header_others(self):
        md = dedent("""
            ## H2

            ### H3

            #### H4

            ##### H5

            ###### H6
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6></div>"
        )


class TestMarkdownBlocksToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



if __name__ == "__main__":
    unittest.main()

