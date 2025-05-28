import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import DEFAULT_SOLUTION_TEMPLATE_NAME
from src.problem import Problem
from src.testing.utils import get_template

CODEFORCES_URL = "https://codeforces.com"
CODEFORCES_PROBLEM_URL_FORMAT = f"{CODEFORCES_URL}/problemset/problem/{{}}/{{}}"
CODEFORCES_PROBLEM_URL_PATTERN = re.compile(
    CODEFORCES_URL + r"/problemset/problem/\d+/[A-Z]"
)


def get_codeforces_problem(problem_id: int, problem_index: str) -> Problem:
    service = Service(executable_path=ChromeDriverManager().install())

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=options)

    url = CODEFORCES_PROBLEM_URL_FORMAT.format(problem_id, problem_index)
    driver.get(url)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    tags = [
        tag.get_text(strip=True).capitalize()
        for tag in soup.find_all("span", class_="tag-box")
    ]
    code_snippet = get_template(DEFAULT_SOLUTION_TEMPLATE_NAME)

    try:
        title = soup.find("div", class_="title").get_text(strip=True)[3:]
    except ValueError:
        title = str(None)

    try:
        difficulty = next(filter(lambda x: x[0] == "*" and x[1:].isdigit(), tags))
        tags.remove(difficulty)
        difficulty = difficulty[1:]
    except StopIteration:
        difficulty = str(None)

    test_cases = []
    for test in soup.find_all("div", class_="sample-test"):
        input_div = test.find("div", class_="input")
        if not input_div:
            continue
        input_pre = input_div.find("pre")
        if not input_pre:
            continue
        input_data = input_pre.get_text("\n")

        output_div = test.find("div", class_="output")
        if not output_div:
            continue
        output_pre = output_div.find("pre")
        if not output_pre:
            continue
        output_data = output_pre.get_text("\n")

        test_cases.append(f"{input_data}\n\n{output_data}")

    return Problem(
        id=problem_id,
        slug=f"{problem_id}{problem_index}",
        url=url,
        title=title,
        difficulty=difficulty,
        content="",
        tags=tags,
        code_snippet=code_snippet,
        test_cases=test_cases,
    )
