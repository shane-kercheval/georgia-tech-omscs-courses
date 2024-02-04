# georgia-tech-omscs-courses

This project scrapes all of the course and specialization information from the OMSCS website, gives it to ChatGPT (along with a resume) and asks it to recommend various options based on past experience, interests, and gaps in knowledge.

# Running the Project

- download and install [Docker](https://www.docker.com/)
- clone repo (`git clone https://github.com/shane-kercheval/georgia-tech-omscs-courses.git`)
- navigate to repo (`cd georgia-tech-omscs-courses/`)
- create `.env` file in project directory with `OPENAI_API_KEY=<your OpenAI API Key>`
- Replace content in `context/resume.txt` with your information.
- Replace content in `context/interests.txt` with your information.
- run `make docker_run` to start docker container
- once, container is started, in another window run `make docker_recommend` (costs about $0.25)

Note that I did not include the `Computational Perception and Robotics` specialization. Uncomment relevant line 10 in omscs.py to include it.
