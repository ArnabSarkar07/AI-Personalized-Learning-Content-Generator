**Problem Statement:** PS-1  
Develop an AI-based system that generates personalized learning content based on a student's topic, subject, self-assessed proficiency level, and previous quiz score.

## Project Overview

This project generates customized learning material for students, including:

- Personalized explanations
- Quick revision notes
- Practice questions
- Difficulty-adjusted content

The system adjusts content difficulty across three levels:

1. Beginner
2. Intermediate
3. Advanced

If a student enters a previous quiz score, the system automatically adjusts the difficulty level:

| Quiz Score | Difficulty Adjustment |
|---|---|
| 80-100 | Move one level higher |
| 40-79 | Keep the same level |
| 0-39 | Move one level lower |

## Technologies Used

- Python
- Flask
- HTML
- CSS
- Rule-based NLP/content-generation logic
- Optional generative AI API integration

## Features

- Student-friendly web interface
- Topic-based personalized content generation
- Proficiency-level selection
- Automatic difficulty adjustment using quiz scores
- Explanation, notes, and practice-question generation
- REST API endpoint for programmatic access
- Lightweight and easy to run

## How to Run

1. Install Python 3.8 or above.
2. Install Flask:


[pip install flask]


3. Run the application:


[python app.py]


4. Open the following URL in a browser:


http://127.0.0.1:5000/


## Sample Inputs and Outputs

### Beginner Level

**Input:**  
Topic: Python Loops  
Subject: Python  
Level: Beginner  

**Output:**  
The system generates a simple explanation, basic revision notes, and easy practice questions.

### Intermediate Level

**Input:**  
Topic: Machine Learning  
Subject: Artificial Intelligence  
Level: Intermediate  

**Output:**  
The system generates a working-process explanation, advantages/limitations, and application-based questions.

### Advanced Level

**Input:**  
Topic: Data Structures  
Subject: Computer Science  
Level: Advanced  

**Output:**  
The system generates optimization-focused explanations, complexity-analysis notes, and higher-order questions.

## Prompt Design and Content Generation Logic

The application uses a structured prompt/template design. The generated content depends on:

- Student topic
- Subject
- Proficiency level
- Previous quiz score

The content-generation logic follows this flow:

```text
Student Input
      |
      v
Topic + Subject + Proficiency Level + Quiz Score
      |
      v
Difficulty Adjustment Engine
      |
      v
Level-Based Content Template
      |
      v
Personalized Explanation + Notes + Practice Questions
```

### Prompt Design

For each level, the system uses a different instructional prompt style:

- **Beginner:** Simple definitions, examples, and basic questions
- **Intermediate:** Working process, comparison, advantages, limitations, and application questions
- **Advanced:** Optimization, complexity, edge cases, trade-offs, and analytical questions

Example internal prompt structure:

```text
Generate a {level} level explanation for the topic "{topic}" in the subject "{subject}".
Include a simple example, revision notes, and practice questions suitable for a {level} learner.
```

## API Usage

Send a POST request to:

```text
/api/generate
```

Example JSON request:

```json
{
  "topic": "Python Loops",
  "subject": "Python",
  "level": "Beginner",
  "quiz_score": 90
}
```

The API returns generated explanation, notes, and practice questions.

## Demo Video
```text
Demo Video Link: https://drive.google.com/file/d/19fPVr2WAXx65UvIVtcaHILaiyL0Qh6XQ/view?usp=sharing     
```

## Future Scope

- Integration with OpenAI, Gemini, or other generative AI APIs
- Student login and progress tracking
- Automatic quiz generation and evaluation
- Recommendation of learning resources
- Support for multiple languages


