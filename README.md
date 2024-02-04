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

# Output

I asked ChatGPT to provide two recommendations on specializations/courses: one that best aligned best with my background and interests, and another that concentrates on address gaps in my knowledge/experience.

It gives fairly solid recommendations. Sometimes it recommends the full 10 courses, and other times it doesn't.

```
shanekercheval@Shanes-MBP georgia-tech-omscs-courses % make docker_recommend

docker compose run --no-deps --entrypoint "make all" bash

python source/cli.py scrape-omscs-courses
Scraping OMSCS course list...
Scraping course overviews and suggested background...
Saving course data to file...
Scraping completed in 2.87 seconds.

python source/cli.py scrape-omscs-specializations
Scraping OMSCS specialization list...
Saving specialization data to file...
Scraping completed in 1.53 seconds.

python source/cli.py recommend
Generating recommendations based on your resume and interests...

### Recommendation 1: Specialization in Machine Learning

Given your extensive background as a Senior Data Scientist and ML Engineer, a specialization in Machine Learning aligns perfectly with your experience and interests, particularly considering your involvement in researching and developing advanced AI products and tools, including LLMs. Your work with Python package dependencies and the implementation of sales forecasting models further underscores your readiness for advanced ML coursework.

**Core/Required Courses:**

1. **CS 6515 Introduction to Graduate Algorithms:** Since you have a strong foundation in programming and software development, this course will solidify your understanding of algorithms, which are crucial for machine learning.
   
   *Preparation*: Brush up on complex algorithm design and analysis to optimize your learning.

2. **CS 7641 Machine Learning:** Directly applicable to your work and interests, this course will deepen your theoretical and practical knowledge of machine learning algorithms.

   *Preparation*: Since you've been in the field for a while, a quick review of the latest ML research and techniques (especially those not directly covered in your current role) can be beneficial.

**Elective Courses:**

3. **CS 7643 Deep Learning:** Given your title change and interest in software-driven projects, this course will augment your skill set in the rapidly evolving field of deep learning.

   *Preparation*: Engage with the latest deep learning frameworks that you haven't worked with as much, such as TensorFlow or PyTorch.

4. **CS 7642 Reinforcement Learning and Decision Making:** This course aligns with solving complex, real-world problems using AI, a key interest of yours.

   *Preparation*: Review Markov Decision Processes and game theory basics, if you're not already familiar.

5. **CS 7646 Machine Learning for Trading:** Combines your interest in programming and ML with an application in trading, expanding your expertise into financial data.

   *Preparation*: Familiarize yourself with basic financial concepts and trading strategies.

6. **CSE 6240 Web Search and Text Mining:** As a Data Scientist, the skills to analyze and derive meaning from web data can complement your ML expertise.

   *Preparation*: Delve into NLP basics if you aren't familiar with them.

7. **CS 6603 AI, Ethics, and Society:** Aligns with your product management experience, highlighting the ethical considerations in AI product development.

   *Preparation*: Engage with recent discussions and publications on AI ethics to bring a well-informed perspective to class discussions.

### Recommendation 2: Specialization in Computing Systems

Focusing on Computing Systems could address your knowledge gaps, particularly gaining a deeper understanding of the systems that power the tools and applications you develop. This specialization would strengthen your comprehensive understanding of both software and hardware aspects necessary for optimized ML engineering and data science work.

**Core/Required Courses:**

1. **CS 6515 Introduction to Graduate Algorithms:** Crucial for understanding the computational complexity and efficiency of data science and ML systems.
   
   *Preparation*: Dive deeper into theoretical CS concepts that you might not engage with daily.

2. **CS 6210 Advanced Operating Systems:** Offers in-depth knowledge of OS, crucial for high-performance computing and AI applications.

   *Preparation*: Review OS principles and experiment with Linux kernel programming.

3. **CS 6290 High-Performance Computer Architecture:** Understanding the hardware that underlies computing will allow you to optimize your ML models and data analysis processes.

   *Preparation*: Brush up on basic computer architecture and familiarize yourself with recent advancements in GPU technology.

**Elective Courses:**

4. **CS 6200 Introduction to Operating Systems:** Reinforces core principles and gives you hands-on experience with OS, complementing CS 6210.

   *Preparation*: Practical exercises in system calls and process management.

5. **CSE 6220 Intro to High-Performance Computing:** Directly improves your ability to work with large datasets and complex models more efficiently.

   *Preparation*: Learn basic parallel programming paradigms.

6. **CS 6300 Software Development Process or CS 6301 Advanced Topics in Software Engineering:** Either of these will deepen your understanding of best practices in software development, an essential skill for any ML project.

   *Preparation*: If opting for 6301, review current software engineering challenges and trends.

7. **CS 6250 Computer Networks:** Enhances your understanding of networked systems, beneficial for cloud-based ML applications.

   *Preparation*: Catch up on TCP/IP stack and experiment with network simulation tools.

By focusing on these two recommended specializations, you'll be able to both leverage your existing strengths and interests in ML while also filling in crucial knowledge gaps related to the underlying systems that power ML and data science technologies.

---

Total Cost:            $0.24457
Total Tokens:          22,517
Total Prompt Tokens:   21,547
Total Response Tokens: 970
Saving recommendations to file: context/recommendations.txt
```
