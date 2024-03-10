import json
from pathlib import Path

import streamlit as st
from streamlit.source_util import _on_pages_changed, get_pages


def get_all_pages(DEFAULT_PAGE):
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page(DEFAULT_PAGE):
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages(DEFAULT_PAGE)

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


def show_all_pages(DEFAULT_PAGE):
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages(DEFAULT_PAGE)

    missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

    # Replace all the missing pages
    for key in missing_keys:
        current_pages[key] = saved_pages[key]

    _on_pages_changed.send()


# clear_all_but_first_page()
#
# st.write("Hello world")
#
# with st.form("Login"):
#     username = st.text_input("Username", "streamlit", key="username")
#     password = st.text_input("Password", "streamlit", type="password", key="password")
#     st.form_submit_button()
#
# if username == "streamlit" and password == "streamlit":
#     show_all_pages()
# else:
#     st.write("Incorrect username or password")
#     clear_all_but_first_page()
