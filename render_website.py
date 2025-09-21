import os
import json
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    load_dotenv()
    with open(os.getenv("DATA_FILE","meta_data.json"), "r", encoding="utf8") as my_file:
        books = json.load(my_file)
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    os.makedirs("pages", exist_ok=True)
    template = env.get_template("template.html")
    page_quantity = 10
    books_pages = list(chunked(books, page_quantity))
    for number, books_page in enumerate(books_pages,start=1):
        rendered_page = template.render(
            books = books_page,
            all_numbers = len(books_pages),
            number_page = number
        )
        with open(f"pages/index{number}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="./pages/index1.html")


if __name__ == "__main__":
    main()