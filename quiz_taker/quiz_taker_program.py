# import necessary libraries for GUI and file handling
import tkinter as tk
from tkinter import messagebox
import random

# define a function to load quiz questions from a text file
def load_quiz_data(filename="quiz_storage.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip()

    blocks = content.split("Question: ")[1:]
    questions = []

    for block in blocks:
        # parse each line in the block to extract questions and options
        lines = block.strip().splitlines()
        question_text = lines[0].strip()
        options = {
            "option_a": lines[2].split("option_a: ")[1].strip(),
            "option_b": lines[3].split("option_b: ")[1].strip(),
            "option_c": lines[4].split("option_c: ")[1].strip(),
            "option_d": lines[5].split("option_d: ")[1].strip(),
        }
        correct_answer = lines[6].split("Correct Answer: ")[1].strip()
        # store the parsed question data into the list
        questions.append({
            "question": question_text,
            "options": options,
            "correct": correct_answer
        })

    #shuffle the list of questions randomly
    random.shuffle(questions)
    return questions
    
# define a class for the quiz application
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #set up the main window
        self.title("🔥 Quiz Taker 🔥")
        self.geometry("800x600")
        self.configure(bg="#222831")

        # load quiz questions and intialize counters
        self.questions = load_quiz_data()
        self.current_index = 0
        self.user_answers = []

        self.create_widgets()
        self.load_question()

    # create the UI components
    def create_widgets(self):
        self.title_label = tk.Label(self, text="QUIZ TIME", font=("Helvetica", 24, "bold"), fg="#FFD369", bg="#222831")
        self.title_label.pack(pady=20)

        self.question_label = tk.Label(self, text="", font=("Helvetica", 16), fg="white", bg="#222831", wraplength=700, justify="center")
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self, bg="#222831")
        self.options_frame.pack(pady=10)

        self.selected_answer = tk.StringVar(value="")

        self.option_buttons = {}
        for key in ['option_a', 'option_b', 'option_c', 'option_d']:

            # create radio buttons for each option
            btn = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_answer,
                value=key,
                font=("Helvetica", 13),
                bg="#393E46",
                fg="white",
                wraplength=650,
                justify="left",
                indicatoron=0,
                width=60,
                height=3,
                pady=10,
                selectcolor="#FFD369",
                activebackground="#00ADB5"
            )
            btn.pack(pady=1, anchor="w")
            self.option_buttons[key] = btn

        #create a submit button
        self.submit_button = tk.Button(self, text="Submit Answer", command=self.submit_answer, font=("Helvetica", 14), bg="#00ADB5", fg="white")
        self.submit_button.pack(pady=20)

    # load the quiz question into the UI
    def load_question(self):
        if self.current_index < len(self.questions):
            current_question = self.questions[self.current_index]
            self.question_label.config(text=current_question["question"])
            self.selected_answer.set("")

            for key, btn in self.option_buttons.items():
                btn.config(text=current_question["options"][key], state=tk.NORMAL)

        else:
            self.show_results()

    # handle the user's answer
    def submit_answer(self):
        selected = self.selected_answer.get()
        # if no option selected, show warning
        if not selected:
            messagebox.showwarning("Warning", "Please select an option.")
            return

        # record selected answer
        self.user_answers.append(selected)
        # move to next question
        self.current_index += 1
        self.load_question()

    # display quiz results
    def show_results(self):
        #clear the window of previous widgets
        for widget in self.winfo_children():
            widget.destroy()

        score = 0
        result_text = ""

        for i, question in enumerate(self.questions):
            correct = question["correct"]
            user_choice = self.user_answers[i]

            if user_choice == correct:
                # increment score if correct
                score += 1
            else:
                # record incorrect answer details
                question_text = question["question"]
                user_answer = question["options"][user_choice]
                correct_answer = question["options"][correct]
                result_text += f"\n🟥 {question_text}\n  ❌ Your Answer: {user_answer}\n  ✅ Correct Answer: {correct_answer}\n"

        # display score summary
        score_summary = f"🏁 Your Score: {score}/{len(self.questions)}\n"
        score_label = tk.Label(self, text=score_summary, font=("Helvetica", 20, "bold"), fg="#FFD369", bg="#222831")
        score_label.pack(pady=20)

        if result_text:
            # show detailed feedback if there were mistakes
            result_box = tk.Text(self, wrap="word", font=("Helvetica", 14), bg="#393E46", fg="white", width=60, height=15)
            result_box.insert(tk.END, result_text.strip())
            result_box.config(state="disabled")
            result_box.pack(pady=10)
        else:
            # display perfect score message
            perfect_label = tk.Label(self, text="🎉 Perfect Score! Galing mo boss!", font=("Helvetica", 16), fg="white", bg="#222831")
            perfect_label.pack(pady=10)

        # add button to restart the quiz
        restart_button = tk.Button(self, text="Try Again", command=self.restart_quiz, font=("Helvetica", 14), bg="#00ADB5", fg="white")
        restart_button.pack(pady=1)

    # function to restart the quiz
    def restart_quiz(self):
        self.questions = load_quiz_data()
        self.current_index = 0
        self.user_answers = []

        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.load_question()

# run the program
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
