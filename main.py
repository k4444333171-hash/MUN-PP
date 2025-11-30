import pdfplumber
import docx
from textblob import TextBlob
import re

# -----------------------------------------
# EXTRACT TEXT FROM FILE
# -----------------------------------------
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith(".docx"):
        d = docx.Document(file_path)
        return "\n".join([p.text for p in d.paragraphs])

    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


# -----------------------------------------
# SCORING FUNCTIONS (RULE BASED)
# -----------------------------------------

def score_understanding(text):
    keywords = ["issue", "problem", "background", "crisis", "topic"]
    score = sum(text.lower().count(k) for k in keywords)
    return min(score, 10)


def score_policy_alignment(text, country):
    policy_keywords = [country.lower(), "delegate", "government", "position", "foreign policy"]
    score = sum(text.lower().count(k) for k in policy_keywords)
    return min(score, 10)


def score_analysis(text):
    analysis_keywords = ["solution", "recommend", "propose", "analysis", "impact"]
    score = sum(text.lower().count(k) for k in analysis_keywords)
    return min(score, 10)


def score_evidence(text):
    numbers = re.findall(r"\d+", text)
    score = len(numbers) // 2  # 1 mark per 2 statistics
    return min(score, 10)


def score_formatting(text):
    sections = ["introduction", "body", "conclusion", "heading", "subheading"]
    score = sum(1 for s in sections if s in text.lower())
    return min(score, 5)


def score_grammar(text):
    blob = TextBlob(text)
    errors = sum(1 for sentence in blob.sentences if sentence.correct() != sentence)
    score = 5 - min(errors // 3, 5)
    return max(score, 0)


# -----------------------------------------
# GENERATE FEEDBACK
# -----------------------------------------

def generate_feedback(score_dict):
    feedback = []

    if score_dict["understanding"] < 5:
        feedback.append("Improve understanding of the topic. Add more background details.")
    if score_dict["policy_alignment"] < 5:
        feedback.append("Add clearer links to your country's foreign policy.")
    if score_dict["analysis"] < 5:
        feedback.append("Provide stronger solutions and analysis.")
    if score_dict["evidence"] < 5:
        feedback.append("Add statistics, dates, treaties, and real facts.")
    if score_dict["formatting"] < 3:
        feedback.append("Improve formatting with headings and structure.")
    if score_dict["grammar"] < 3:
        feedback.append("Work on grammar and clarity of writing.")

    if not feedback:
        feedback.append("Excellent position paper. Well-structured and detailed!")

    return feedback


# -----------------------------------------
# MAIN FUNCTION
# -----------------------------------------

def evaluate_paper(file_path, delegate, country, committee):
    text = extract_text(file_path)

    scores = {
        "understanding": score_understanding(text),
        "policy_alignment": score_policy_alignment(text, country),
        "analysis": score_analysis(text),
        "evidence": score_evidence(text),
        "formatting": score_formatting(text),
        "grammar": score_grammar(text),
    }

    scores["overall"] = (
        scores["understanding"] +
        scores["policy_alignment"] +
        scores["analysis"] +
        scores["evidence"] +
        scores["formatting"] +
        scores["grammar"]
    )

    feedback = generate_feedback(scores)

    print("\n==== MUN POSITION PAPER EVALUATION (OFFLINE) ====")
    print(f"Delegate: {delegate}")
    print(f"Country: {country}")
    print(f"Committee: {committee}\n")

    print("----- SCORES -----")
    for k, v in scores.items():
        print(f"{k.capitalize()}: {v}")

    print("\nOverall Score:", scores["overall"], "/ 50")

    print("\n----- FEEDBACK -----")
    for f in feedback:
        print("- " + f)


# -----------------------------------------
# RUN
# -----------------------------------------

if __name__ == "__main__":
    file_path = input("Enter file path: ")
    delegate = input("Delegate Name: ")
    country = input("Country: ")
    committee = input("Committee: ")

    evaluate_paper(file_path, delegate, country, committee)
