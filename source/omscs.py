"""Contains functions to scrape the OMSCS website for course and specialization information."""
import aiohttp
import requests
from bs4 import BeautifulSoup


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

def get_specialization_info(url: str) -> tuple[str, str]:  # noqa: PLR0912
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

    # scrape core courses for the specialization
    core_courses_heading = soup.find('h3', string=lambda x: 'Core Courses' in x)
    if core_courses_heading:
        next_sibling = core_courses_heading.find_next_sibling()
        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name == 'ul':
                list_items = next_sibling.find_all('li')
                for item in list_items:
                    core_courses_text += item.get_text().strip() + '\n'
            elif next_sibling.name == 'p':
                core_courses_text += next_sibling.get_text().strip() + '\n'
            else:
                core_courses_text += next_sibling.string.strip() + '\n'
            next_sibling = next_sibling.find_next_sibling()

    # scrape elective courses for the specialization
    electives_heading = soup.find('h3', string=lambda x: 'Electives' in x)
    if electives_heading:
        next_sibling = electives_heading.find_next_sibling()
        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name == 'p':
                elective_courses_text += next_sibling.get_text().strip() + '\n'
            elif next_sibling.name == 'ul':
                list_items = next_sibling.find_all('li')
                for item in list_items:
                    if item.find('a'):
                        course_link = item.find('a')['href']
                        course_name = item.find('strong').get_text(strip=True)
                        elective_courses_text += f"{course_name} [{course_link}]".strip() + '\n'
                    else:
                        elective_courses_text += item.get_text(strip=True).strip() + '\n'
            else:
                elective_courses_text += next_sibling.string + '\n'
            next_sibling = next_sibling.find_next_sibling()

    return core_courses_text.strip(), elective_courses_text.strip()

def format_specializations(info: dict) -> str:
    """Format the specializations information into a human-readable string (passed to ChatGPT)."""
    formatted_str = ""
    for specialization, courses in info.items():
        formatted_str += f"SPECIALIZATION: {specialization}\n\n"
        formatted_str += "CORE/REQUIRED COURSES:\n"
        formatted_str += f"{courses['core_courses']}\n\n"
        formatted_str += "ELECTIVES:\n"
        formatted_str += f"{courses['elective_courses']}\n\n\n\n"
    return formatted_str.strip()

def format_courses(info: dict) -> str:
    """Format the courses information into a human-readable string (passed to ChatGPT)."""
    formatted_str = ""
    for course, details in info.items():
        formatted_str += f"COURSE: {course}\n"
        # formatted_str += f"URL: {details['url']}\n"
        formatted_str += f"OVERVIEW:\n{details['overview']}\n"
        formatted_str += f"SUGGESTED BACKGROUND:\n{details['suggested_background']}\n\n\n"
    return formatted_str.strip()
