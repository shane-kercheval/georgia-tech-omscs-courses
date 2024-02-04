"""
Scrapes all of the course and specialization information from the OMSCS website, gives
it to ChatGPT (along with a resume) and asks it to recommend various options based on past
experience, interests, and gaps in knowledge.
"""

import time
import asyncio
import click
import yaml
from llm_workflow.openai import OpenAIChat
from source.omscs import (
    OMSCS_SPECIALIZATIONS,
    format_courses,
    format_specializations,
    get_course_overview,
    get_omscs_current_courses,
    get_specialization_info,
)
from dotenv import load_dotenv
load_dotenv()


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

@main.command()
def recommend() -> None:
    """Recommend courses and specializations based on user input."""
    with open('scraped/omscs_courses.yaml') as f:
        courses = yaml.safe_load(f)
    with open('scraped/omscs_specializations.yaml') as f:
        specializations = yaml.safe_load(f)
    with open('context/resume.txt') as f:
        resume = f.read()
    with open('context/interests.txt') as f:
        interests = f.read()
    with open('context/prompt.txt') as f:
        prompt = f.read()

    prompt = prompt.\
        replace('{{resume}}', resume).\
        replace('{{interests}}', interests).\
        replace('{{specialization}}', format_specializations(specializations)).\
        replace('{{courses}}', format_courses(courses))

    chat = OpenAIChat(
        model_name='gpt-4-0125-preview',
        streaming_callback=lambda x: print(x.response, end='', flush=True),
    )
    print("Generating recommendations based on your resume and interests...")
    response = chat(prompt)
    print("\n\n---\n\n")
    print(f"Total Cost:            ${chat.cost:.5f}")
    print(f"Total Tokens:          {chat.total_tokens:,}")
    print(f"Total Prompt Tokens:   {chat.input_tokens:,}")
    print(f"Total Response Tokens: {chat.response_tokens:,}")
    rec_file = 'context/recommendations.txt'
    print(f"Saving recommendations to file: {rec_file}")
    with open(rec_file, 'w') as f:
        f.write(response)


if __name__ == "__main__":
    main()
