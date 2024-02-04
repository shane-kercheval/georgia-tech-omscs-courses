"""
Scrapes all of the course and specialization information from the OMSCS website, gives
it to ChatGPT (along with a resume) and asks it to recommend various options based on past
experience, interests, and gaps in knowledge.
"""

import time
import requests
import aiohttp
import asyncio
import click
from bs4 import BeautifulSoup
import yaml


OMSCS_CURRENT_COURSES_URL = 'https://omscs.gatech.edu/current-courses'
OMSCS_SPECIALIZATIONS = {
    # not including Computational Perception and Robotics
    # 'Computational Perception and Robotics': {'url': 'https://omscs.gatech.edu/specialization-computational-perception-robotics'},
    'Computing Systems': {'url': 'https://omscs.gatech.edu/specialization-computing-systems'},
    'Human Computer Interaction': {'url': 'https://omscs.gatech.edu/specialization-human-computer-interaction'},
    'Interactive Intelligence': {'url': 'https://omscs.gatech.edu/specialization-interactive-intelligence'},
    'Machine Learning': {'url': 'https://omscs.gatech.edu/specialization-machine-learning'},
}


def get_omscs_current_courses() -> dict:
    """
    Retrieves the current OMSCS courses from the OMSCS website and returns a dictionary with the
    course name as the key and a nested dictionary with the course URL as the value.
    """
    response = requests.get(OMSCS_CURRENT_COURSES_URL)
    assert response.status_code == 200, f"Failed to retrieve page. Status: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    section = soup.find('h3', string="Current & Ongoing OMS Courses").find_next('ul')
    link_elements = section.find_all('a')
    return {
        link.text.strip(): {'url': link.get('href')}
        for link in link_elements if link.get('href')
    }

async def get_course_overview(url: str) -> tuple[str, str]:
    """
    Retrieves the course overview and suggested background from the OMSCS website and returns it as
    a string.

    Args:
        url: The URL of the course to scrape.
    """
    overview_text = ""
    suggested_background_text = ""

    async with \
        aiohttp.ClientSession() as session, \
        session.get(url) as response:
            assert response.status == 200, \
                f"Failed to retrieve page `{url}`. Status: {response.status}"
            course_content = await response.text()

    course_soup = BeautifulSoup(course_content, 'html.parser')
    overview_section = course_soup.find('h4', string="Overview")
    assert overview_section, f"Failed to find 'Overview' section for {url}"

    current_element = overview_section.find_next_sibling()
    while current_element and current_element.name != 'h4':
        if current_element.name == 'p':
            overview_text += current_element.text + "\n"
        elif current_element.name == 'ul':
            for item in current_element.find_all('li'):
                overview_text += item.text + "\n"
        current_element = current_element.find_next_sibling()
    overview_text = overview_text.strip()

    suggested_background_section = course_soup.find('h4', string="Before Taking This Class...")
    if suggested_background_section:
        suggested_background_text = suggested_background_section.find_next('p').text.strip()

    return overview_text, suggested_background_text

def get_specialization_info(url: str) -> tuple[str, str]:
    """
    Retrieves the specialization core and elective courses from the OMSCS website and returns
    each as a string in a tuple.

    Args:
        url: The URL of the specialization to scrape.
    """
    core_courses_text = ""
    elective_courses_text = ""

    response = requests.get(url)
    assert response.status_code == 200, \
        f"Failed to retrieve page `{url}`. Status: {response.status_code}"
    soup = BeautifulSoup(response.text, 'html.parser')
    core_courses_heading = soup.find('h3', string=lambda x: 'Core Courses' in x)
    if core_courses_heading:
        next_sibling = core_courses_heading.find_next_sibling()
        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name == 'ul':
                list_items = next_sibling.find_all('li')
                for item in list_items:
                    core_courses_text += item.get_text() + '\n'
            elif next_sibling.name == 'p':
                core_courses_text += next_sibling.get_text() + '\n'
            else:
                core_courses_text += next_sibling.string + '\n'
            next_sibling = next_sibling.find_next_sibling()
    return core_courses_text.strip(), elective_courses_text.strip()

def run_async_tasks(tasks: list[asyncio.Task]) -> list[object]:
    """Runs the given async tasks and returns the results."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(asyncio.gather(*tasks))

@click.group()
def main() -> None:
    """Runs the program."""
    pass

@main.command()
def scrape_omscs_courses() -> None:
    """Scrape the current courses, course overview, and suggested background from OMSCS website."""
    start = time.time()
    print("Scraping OMSCS course list...")
    courses = get_omscs_current_courses()
    tasks = [get_course_overview(info['url']) for _, info in courses.items()]
    print("Scraping course overviews and suggested background...")
    results = run_async_tasks(tasks)

    for (name, _), result in zip(courses.items(), results):
        overview, suggested_background = result
        courses[name]['overview'] = overview
        courses[name]['suggested_background'] = suggested_background

    print("Saving course data to file...")
    with open('scraped/omscs_courses.yaml', 'w') as file:
        file.write(yaml.dump(courses))

    finish = time.time()
    print(f"Scraping completed in {finish - start:.2f} seconds.")

@main.command()
def scrape_omscs_specializations() -> None:
    """Scrape the specialization core and elective courses from OMSCS website."""
    start = time.time()
    print("Scraping OMSCS specialization li,st...")
    specializations = {}
    for name, info in OMSCS_SPECIALIZATIONS.items():
        core, elective = get_specialization_info(info['url'])
        specializations[name] = {
            'core_courses': core,
            'elective_courses': elective
        }

    print("Saving specialization data to file...")
    with open('scraped/omscs_specializations.yaml', 'w') as file:
        file.write(yaml.dump(specializations))

    finish = time.time()
    print(f"Scraping completed in {finish - start:.2f} seconds.")
    
if __name__ == "__main__":
    main()
