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

class QuizCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Creator")
        self.geometry("700x700")
        self.config(bg="#FFEB3B")

        # fonts and colors
        self.font_main = ("Arial", 12)
        self.font_title = ("Arial", 16, "bold")
        self.bg_color = "#FF5722"
        self.bg_color2 = "#FF9800"

        # add tabs using a notebook widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # create the tabs for "Create" and "View/Edit"
        self.create_tab = tk.Frame(self.notebook, bg="#FF9800")
        self.view_tab = tk.Frame(self.notebook, bg="#FF9800")
        self.notebook.add(self.create_tab, text="Create Question")
        self.notebook.add(self.view_tab, text="View/Edit Questions")
        
        # create question tab UI
        self.create_question_ui()

        # view/edit questions tab UI
        self.view_edit_ui()

        self.question_count = self.get_question_count()

    def create_question_ui(self):
        # labels and inputs for creating questions
        tk.Label(self.create_tab, text="Enter Quiz Question:", font=self.font_title, bg="#FFEB3B").pack(pady=10)
        self.question_entry = tk.Entry(self.create_tab, font=self.font_main, width=50)
        self.question_entry.pack(pady=5)

        tk.Label(self.create_tab, text="Enter Options:", font=self.font_title, bg="#FFEB3B").pack(pady=10)
        self.options = {}
        for choice in ['option_a', 'option_b', 'option_c', 'option_d']:
            label = choice
            self.options[choice] = tk.Entry(self.create_tab, font=self.font_main, width=50)
            tk.Label(self.create_tab, text=label, font=self.font_main, bg="#FFEB3B").pack(pady=5)
            self.options[choice].pack(pady=5)
        
        tk.Label(self.create_tab, text="Select Correct Answer:", font=self.font_title, bg="#FFEB3B").pack(pady=10)
        self.correct_answer = ttk.Combobox(self.create_tab, values=['option_a', 'option_b', 'option_c', 'option_d'], font=self.font_main, state="readonly")
        self.correct_answer.pack(pady=5)

        # save question button
        self.save_button = tk.Button(self.create_tab, text="Save Question", font=self.font_main, bg=self.bg_color, command=self.save_question)
        self.save_button.pack(pady=10)
    
    def save_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Error", "Please enter a question.")
            return

        options = {key: entry.get().strip() for key, entry in self.options.items()}
        if not all(options.values()):
            messagebox.showwarning("Error", "Please enter all options.")
            return

        correct_answer = self.correct_answer.get()
        if not correct_answer:
            messagebox.showwarning("Error", "Please select a correct answer.")
            return

        filename = "quiz_storage.txt"
        self.question_count += 1
        block = format_question_block(question, options, correct_answer)
        save_question_to_file(filename, block)

        messagebox.showinfo("Success", "Question saved successfully!")
        self.clear_inputs()
        self.load_questions()

    def clear_inputs(self):
        self.question_entry.delete(0, tk.END)
        for entry in self.options.values():
            entry.delete(0, tk.END)
        self.correct_answer.set('')

    def get_question_count(self):
        if not os.path.exists("quiz_storage.txt"):
            return 0
        with open("quiz_storage.txt", "r", encoding="utf-8") as file:
            return sum(1 for line in file if line.startswith("[QUESTION"))
    
    def view_edit_ui(self):
        self.question_display = ScrolledText(self.view_tab, width=70, height=25, font=self.font_main)
        self.question_display.pack(pady=10)
        self.load_questions()

        self.edit_button = tk.Button(self.view_tab, text="Edit Question (Paste it first)", font=self.font_main, bg=self.bg_color, command=self.edit_question)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.view_tab, text="Delete All Questions", font=self.font_main, bg=self.bg_color2, command=self.delete_question)
        self.delete_button.pack(pady=10)
        
    def load_questions(self):
        self.question_display.delete(1.0, tk.END)
        if os.path.exists("quiz_storage.txt"):
            with open("quiz_storage.txt", "r", encoding="utf-8") as file:
                self.question_display.insert(tk.END, file.read())
        else:
            self.question_display.insert(tk.END, "No questions found.")
    
    def edit_question(self):
        original_text = self.question_display.get("1.0", tk.END).strip()
        if not original_text:
            messagebox.showwarning("No Content", "Nothing to edit.")
            return

        with open("quiz_storage.txt", "w", encoding="utf-8") as file:
            file.write(original_text)
        messagebox.showinfo("Saved", "Changes saved to quiz_storage.txt!")
        self.load_questions()

    def delete_question(self):
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete ALL questions?"):
            open("quiz_storage.txt", "w").close()
            messagebox.showinfo("Deleted", "All questions have been deleted.")
            self.load_questions()