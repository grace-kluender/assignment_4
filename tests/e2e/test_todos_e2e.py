import time
from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:5000"


def test_add_and_delete_todo(page: Page):
    title = f"e2e todo {int(time.time())}"

    # Add todo
    page.goto(f"{BASE_URL}/add_item")
    page.fill('input[name="title"]', title)
    page.click('button[type="submit"]')

    # Confirm new todo on landing page
    page.goto(f"{BASE_URL}/")
    expect(page.get_by_text(title)).to_be_visible()
    page.screenshot(path="artifacts/e2e/after_add.png")

    # Delete todo
    page.goto(f"{BASE_URL}/delete_item")
    page.select_option("select", label=title)
    page.click('button[type="submit"]')

    # Confirm deleted todo is gone
    page.goto(f"{BASE_URL}/")
    expect(page.get_by_text(title)).to_have_count(0)
    page.screenshot(path="artifacts/e2e/after_delete.png")

