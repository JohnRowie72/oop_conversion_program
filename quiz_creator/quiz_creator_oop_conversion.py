import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import os

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer

    def format_for_file(self):
        block = f"Question: {self.text}\n"
        block += "[OPTIONS]\n"
        for key, value in self.options.items():
            block += f"{key}: {value}\n"
        block += f"Correct Answer: {self.correct_answer}\n"
        return block

class QuestionStorage:
    def __init__(self, filename="quiz_storage.txt"):
        self.filename = filename

    def save_question(self, question: Question):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(question.format_for_file())

    def load_questions(self):
        if not os.path.exists(self.filename):
            return "No questions found."
        with open(self.filename, "r", encoding="utf-8") as file:
            return file.read()

    def overwrite_questions(self, content: str):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(content)

    def delete_all_questions(self):
        open(self.filename, "w").close()

    def get_question_count(self):
        if not os.path.exists(self.filename):
            return 0
        with open(self.filename, "r", encoding="utf-8") as file:
            return sum(1 for line in file if line.startswith("Question:"))
