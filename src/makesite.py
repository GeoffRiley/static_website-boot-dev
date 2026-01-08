import os
import shutil

from blocks_markdown import markdown_to_html_node


def copy_directory_contents(source_dir, dest_dir):
    cwd = os.getcwd()
    src_dir_path = os.path.join(cwd, source_dir)
    dest_dir_path = os.path.join(cwd, dest_dir)

    if not os.path.exists(src_dir_path):
        raise Exception("Folder path not existed!")

    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    os.mkdir(dest_dir_path)

    src_dir = os.listdir(src_dir_path)
    for item in src_dir:
        cur_path = os.path.join(src_dir_path, item)
        if os.path.isfile(cur_path):
            shutil.copy(cur_path, dest_dir_path)
        else:
            new_des_dir_path = os.path.join(dest_dir_path, item)
            os.mkdir(new_des_dir_path)
            copy_directory_contents(cur_path, new_des_dir_path)


def _extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        temp = line.lstrip()
        if temp.startswith("# "):
            title = temp[2:]
            title = title.strip()
            return title

    raise Exception("No h1 title found in markdown")


def _generate_page(from_path, template_path, dest_path, base_path=None):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    root = markdown_to_html_node(markdown)
    html_content = root.to_html()
    title = _extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)

    if base_path is None:
        base_path = "/"

    page = page.replace('href="/', f'href="{base_path}')
    page = page.replace('src="/', f'src="{base_path}')

    dir_path = os.path.dirname(dest_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path=None):
    entries = os.listdir(dir_path_content)

    for name in entries:
        src_path = os.path.join(dir_path_content, name)
        if not os.path.isfile(src_path):
            new_dest_dir = os.path.join(dest_dir_path, name)
            if not os.path.exists(new_dest_dir):
                os.mkdir(new_dest_dir)
            generate_pages_recursive(src_path, template_path, new_dest_dir, base_path)
        else:
            if name.endswith(".md"):
                new_name = name.replace(".md", ".html")
                new_dest_path = os.path.join(dest_dir_path, new_name)
                _generate_page(src_path, template_path, new_dest_path, base_path)
