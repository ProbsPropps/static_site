import os
import shutil
import re
from blocks import markdown_to_html_node

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(project_root, "static")
    dest_dir = os.path.join(project_root, "public")

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    content_dir = os.path.join(project_root, "content")
    copy_source_dic_to_public(source_dir, dest_dir)
    generate_pages_recursive(content_dir, "template.html", dest_dir, content_dir)

def copy_source_dic_to_public(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
           # print(f"Copying file {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        
        else:
            #print(f"Creating directory: {dest_path}")
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            copy_source_dic_to_public(source_path, dest_path)
        pass

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        strip = re.match(r"^#\s+(.*)", line)
        if strip:
            return strip.group(1)
    else:
        raise Exception("No main header/title")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        contents_from = file.read()

    with open(template_path, 'r') as file:
        contents_template = file.read()

    html_from = markdown_to_html_node(contents_from).to_html()

    from_title = extract_title(contents_from)

    replaced = contents_template.replace("{{ Title }}", from_title).replace("{{ Content }}", html_from)

    directory = os.path.dirname(dest_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, 'w') as file:
        file.write(replaced)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, content_dir):
    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)
        if os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, dest_dir_path, content_dir)
        elif os.path.isfile(full_path) and full_path.endswith(".md"):
            new_path = os.path.relpath(full_path, content_dir)
            print(new_path)
            passing_path = os.path.join(dest_dir_path, new_path.replace(".md", ".html"))
            os.makedirs(os.path.dirname(passing_path), exist_ok=True)
            generate_page(full_path, template_path, passing_path)
    

if __name__ == "__main__":
    main()