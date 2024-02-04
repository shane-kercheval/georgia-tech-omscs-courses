"""
Scrapes all of the course and specialization information from the OMSCS website, gives
it to ChatGPT (along with a resume) and asks it to recommend various options based on past
experience, interests, and gaps in knowledge.
"""

import time
import asyncio
import click
import yaml
from source.omscs import (
    OMSCS_SPECIALIZATIONS,
    get_course_overview,
    get_omscs_current_courses,
    get_specialization_info,
)


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
    print("Scraping OMSCS specialization list...")
    specializations = {}
    for name, info in OMSCS_SPECIALIZATIONS.items():
        core, electives = get_specialization_info(info['url'])
        specializations[name] = {
            'core_courses': core,
            'elective_courses': electives,
        }

    print("Saving specialization data to file...")
    with open('scraped/omscs_specializations.yaml', 'w') as file:
        file.write(yaml.dump(specializations))

    finish = time.time()
    print(f"Scraping completed in {finish - start:.2f} seconds.")

# @main.command()
# def format_into_

if __name__ == "__main__":
    main()
