#!/usr/bin/env python3
"""Build a compact, bilingual printable study guide from dataset.json."""

from __future__ import annotations

import html
import json
import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_PATH = PROJECT_ROOT / "dataset.json"
HTML_PATH = PROJECT_ROOT / "einbuergerungstest-study-guide.html"
PRACTICE_HTML_PATH = PROJECT_ROOT / "einbuergerungstest-study-guide-without-answers.html"


def require_valid_question(question: dict[str, object]) -> None:
    options = question.get("options")
    translations = question.get("options_trans")
    correct_answer = question.get("correctAnswer")

    if not isinstance(options, list) or len(options) != 4:
        raise ValueError(f"Question {question.get('id')} must have four answer options.")
    if not isinstance(translations, list) or len(translations) != 4:
        raise ValueError(f"Question {question.get('id')} must have four English answer translations.")
    if not isinstance(correct_answer, int) or correct_answer not in range(1, 5):
        raise ValueError(f"Question {question.get('id')} has an invalid correct answer.")


def text(value: object) -> str:
    return html.escape(str(value), quote=False)


def render_question(question: dict[str, object], show_correct_answers: bool) -> str:
    require_valid_question(question)
    options = question["options"]
    translations = question["options_trans"]
    correct_answer = question["correctAnswer"]

    image_markup = ""
    image_name = question.get("img")
    if image_name:
        image_markup = f'<img class="question-image" src="imgs/{html.escape(str(image_name))}" alt="Question illustration">'

    answer_markup = []
    for option_number, (option, translation) in enumerate(zip(options, translations), start=1):
        is_correct = " correct" if show_correct_answers and option_number == correct_answer else ""
        letter = chr(64 + option_number)
        answer_markup.append(
            f'<div class="answer{is_correct}"><span class="answer-letter">{letter}</span>'
            f'<span class="answer-german">{text(option)}</span> '
            f'<span class="answer-english">{text(translation)}</span></div>'
        )

    return f'''<article class="question-card">
  <div class="question-german"><span class="question-number">{text(question['id'])}.</span> {text(question['question'])}</div>
  <div class="question-english">{text(question['question_trans'])}</div>
  {image_markup}
  <div class="answers">{''.join(answer_markup)}</div>
</article>'''


def build_html(questions: list[dict[str, object]], show_correct_answers: bool) -> str:
    question_markup = "\n".join(
        render_question(question, show_correct_answers) for question in questions
    )
    answer_note = (
        "The green-highlighted choice is correct."
        if show_correct_answers
        else "Correct answers are intentionally not marked."
    )
    running_header_note = (
        "Correct answers are highlighted"
        if show_correct_answers
        else "Practice copy: answers are not marked"
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Einbürgerungstest Bilingual Study Guide</title>
  <style>
    @page {{
      size: A4 landscape;
      margin: 10mm 9mm 10mm;
      @top-left {{ content: "Einbürgerungstest · Bilingual Study Guide"; color: #475569; font-size: 6.5pt; }}
      @top-right {{ content: "{running_header_note}"; color: #475569; font-size: 6.5pt; }}
      @bottom-right {{ content: counter(page); color: #475569; font-size: 6.5pt; }}
    }}

    * {{ box-sizing: border-box; }}
    body {{
      color: #111827;
      font-family: "DejaVu Sans", Arial, sans-serif;
      font-size: 6.5pt;
      line-height: 1.12;
      margin: 0;
    }}
    .guide-heading {{
      border-bottom: 0.6pt solid #64748b;
      color: #0f172a;
      font-size: 10.5pt;
      font-weight: 700;
      margin: 0 0 2.8mm;
      padding-bottom: 1.2mm;
    }}
    .guide-note {{
      color: #475569;
      font-size: 6.3pt;
      font-style: italic;
      margin: 0 0 3mm;
    }}
    .questions {{
      column-count: 2;
      column-gap: 7mm;
      column-fill: auto;
    }}
    .question-card {{
      break-inside: avoid;
      border-bottom: 0.25pt solid #cbd5e1;
      margin: 0 0 2.15mm;
      padding: 0 0 1.75mm;
    }}
    .question-german {{
      font-size: 7.1pt;
      font-weight: 700;
      line-height: 1.15;
    }}
    .question-number {{ color: #1d4ed8; }}
    .question-english {{
      color: #475569;
      font-size: 6.25pt;
      font-style: italic;
      line-height: 1.1;
      margin: 0.6mm 0 0.95mm;
    }}
    .question-image {{
      display: block;
      margin: 0.8mm auto 1mm;
      max-height: 33mm;
      max-width: 95%;
    }}
    .answer {{
      display: block;
      font-size: 6.35pt;
      line-height: 1.12;
      padding: 0.22mm 0.7mm;
    }}
    .answer-letter {{
      color: #1e3a8a;
      display: inline-block;
      font-weight: 700;
      width: 3.5mm;
    }}
    .answer-english {{ color: #64748b; font-style: italic; }}
    .answer.correct {{
      background: #e8f5ea;
      border-left: 1.4pt solid #15803d;
      font-weight: 700;
      margin: 0.25mm 0;
      padding-left: 1mm;
    }}
    .answer.correct .answer-letter {{ color: #166534; }}
  </style>
</head>
<body>
  <h1 class="guide-heading">Einbürgerungstest: 310 bilingual study questions</h1>
  <p class="guide-note">German question and answer choices followed by their English translations. {answer_note}</p>
  <main class="questions">
{question_markup}
  </main>
</body>
</html>'''


def main() -> None:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--hide-correct-answers",
        action="store_true",
        help="Generate a practice copy without correct-answer highlighting.",
    )
    arguments = argument_parser.parse_args()

    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    questions = dataset.get("questions")
    if not isinstance(questions, list) or len(questions) != 310:
        raise ValueError("dataset.json must contain exactly 310 questions.")

    output_path = PRACTICE_HTML_PATH if arguments.hide_correct_answers else HTML_PATH
    output_path.write_text(
        build_html(questions, show_correct_answers=not arguments.hide_correct_answers),
        encoding="utf-8",
    )
    print(f"Wrote {output_path.name} with {len(questions)} questions.")


if __name__ == "__main__":
    main()
