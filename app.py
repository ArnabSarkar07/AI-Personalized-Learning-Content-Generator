
from flask import Flask, render_template, request, jsonify
import random, os, json, re

app = Flask(__name__)

# ---------------- Difficulty Engine ----------------
LEVELS = ["Beginner", "Intermediate", "Advanced"]

def normalize_level(level):
    level = (level or "").strip().lower()
    if level in ["1", "beginner", "low", "weak"]:
        return "Beginner"
    if level in ["2", "intermediate", "medium", "average"]:
        return "Intermediate"
    if level in ["3", "advanced", "high", "strong"]:
        return "Advanced"
    return "Beginner"

def adjust_level(current_level, quiz_score):
    """Moves the learner up/down based on quiz performance."""
    current_level = normalize_level(current_level)
    idx = LEVELS.index(current_level)
    if quiz_score >= 80:
        idx = min(idx + 1, len(LEVELS) - 1)
    elif quiz_score < 40:
        idx = max(idx - 1, 0)
    return LEVELS[idx]  

# ---------------- Content Generation Logic ----------------
# Template-based NLP-style generation. Replace with an LLM API if desired.
TEMPLATES = {
    "Beginner": {
"explanation": (                                
            "Let us understand **{topic}** in the simplest way.\n\n"
            "{topic} is an important concept in {subject}. "
            "Think of it as a basic building block that helps us solve problems step by step.\n\n"
            "**Simple example:** {example}\n\n"
            "**Key idea:** Focus first on understanding what {topic} means, why it is used, and how one small example works."
        ),
        "notes": [
            "Definition of {topic} in simple words",
            "Why {topic} is useful in {subject}",
            "One easy real-life or programming example",
            "Common beginner mistakes to avoid",
            "Practice one small problem related to {topic}"
        ],
        "questions": [
            "Define {topic} in your own words.",
            "Give one simple example where {topic} can be used.",
            "What is the main purpose of {topic}?",
            "Match the following: {topic} with its basic use case.",
            "True or False: {topic} is only useful for advanced learners."
        ]
    },
    "Intermediate": {
        "explanation": (
            "At an intermediate level, **{topic}** can be understood through its working process.\n\n"
            "{topic} is used in {subject} to improve how we organize, analyze, or solve a problem. "
            "It becomes more useful when we understand its inputs, process, and output.\n\n"
            "**Example:** {example}\n\n"
            "**Important points:**\n"
            "- Identify the problem where {topic} is applicable.\n"
            "- Understand the step-by-step working method.\n"
            "- Compare it with a simpler alternative.\n"
            "- Analyze its advantages and limitations."
        ),
        "notes": [
            "Working principle of {topic}",
            "Input, process, and output of {topic}",
            "Advantages and limitations of {topic}",
            "Comparison with a related concept in {subject}",
            "Medium-level application-based questions"
        ],
        "questions": [
            "Explain the working process of {topic} with an example.",
            "What are two advantages and two limitations of {topic}?",
            "Differentiate {topic} from a closely related concept.",
            "Solve this application-based question: {question_hint}",
            "Explain how {topic} can improve decision-making in {subject}."
        ]
    },
    "Advanced": {
        "explanation": (
            "At an advanced level, **{topic}** should be analyzed using practical, optimization-based, and critical-thinking perspectives.\n\n"
            "In {subject}, {topic} is not only a concept but also a technique for handling complex problems efficiently. "
            "A strong learner should evaluate correctness, efficiency, scalability, and real-world constraints.\n\n"
            "**Example:** {example}\n\n"
            "**Advanced focus:**\n"
            "- Analyze the time and space complexity where applicable.\n"
            "- Identify edge cases and failure conditions.\n"
            "- Optimize the approach using suitable data structures or algorithms.\n"
            "- Justify design choices using trade-offs."
        ),
        "notes": [
            "Advanced working mechanism of {topic}",
            "Complexity analysis and optimization strategies",
            "Edge cases, constraints, and failure scenarios",
            "Real-world use cases and trade-offs",
            "Research-oriented or project-based extension of {topic}"
        ],
        "questions": [
            "Analyze the efficiency of {topic} for a large dataset.",
            "Identify two edge cases where {topic} may fail or perform poorly.",
            "Propose an improved version of {topic} and justify your modification.",
            "Solve this higher-order question: {question_hint}",
            "Compare {topic} with an alternative approach and recommend the better solution with reasons."
        ]
    }
}

EXAMPLES = {
    "python": "If a student wants to learn Python loops, start with printing numbers from 1 to 5 using a for loop.",
    "machine learning": "If a student wants to learn machine learning, start with classifying emails as spam or not spam.",
    "data structures": "If a student wants to learn data structures, start with storing student marks in a list.",
    "ai": "If a student wants to learn AI, start with a chatbot that answers frequently asked questions.",
    "nlp": "If a student wants to learn NLP, start with counting frequent words in a paragraph."
}

def get_example(topic, subject):
    key = topic.strip().lower()
    for k, v in EXAMPLES.items():
        if k in key:
            return v
    return f"If a student wants to learn {topic}, start with one small, practical example from {subject}."

def generate_content(topic, subject, level):
    level = normalize_level(level)
    t = TEMPLATES[level]
    data = {
        "topic": topic.strip().title(),
        "subject": subject.strip().title(),
        "example": get_example(topic, subject),
        "question_hint": f"Apply {topic.strip()} to a realistic problem in {subject.strip()}."
    }
    explanation = t["explanation"].format(**data)
    notes = [n.format(**data) for n in t["notes"]]
    questions = [q.format(**data) for q in t["questions"]]
    return {
        "level": level,
        "explanation": explanation,
        "notes": notes,
        "practice_questions": questions
    }

# ---------------- Routes ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic", "").strip()
    subject = request.form.get("subject", "").strip() or "Computer Science"
    level = request.form.get("level", "Beginner")
    quiz_score = request.form.get("quiz_score", "")

    if not topic:
        return render_template("index.html", error="Please enter a topic.")

    # Optional quiz-score based adjustment
    if quiz_score:
        try:
            score = int(quiz_score)
            if 0 <= score <= 100:
                level = adjust_level(level, score)
        except ValueError:
            pass

    content = generate_content(topic, subject, level)
    return render_template("index.html", content=content, topic=topic, subject=subject,
                           selected_level=level, quiz_score=quiz_score)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()
    subject = data.get("subject", "Computer Science")
    level = data.get("level", "Beginner")
    quiz_score = data.get("quiz_score")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    if quiz_score is not None:
        try:
            level = adjust_level(level, int(quiz_score))
        except (TypeError, ValueError):
            pass

    return jsonify(generate_content(topic, subject, level))

if __name__ == "__main__":
    app.run(debug=True)
