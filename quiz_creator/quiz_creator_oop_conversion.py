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

