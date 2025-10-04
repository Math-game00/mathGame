from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import random
import math


class MathGameWithCustomBackground:
    def __init__(self, root):
        self.root = root
        self.root.title("เกม คณิต คิด หรรษา")
        self.root.geometry("800x600")
        self.root.config(bg="#eb9bae")  # สีชมพูอ่อน
        self.root.resizable(True, True)
        # ตั้งค่าเกม
        self.start_bg_image = Image.open("math.jpg")  # ภาพเริ่มต้น
       
        self.start_bg_photo = None
        self.game_bg_photo = None

        # สร้าง Canvas
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # ใส่พื้นหลังภาพเริ่มต้น
        self.start_bg_photo = ImageTk.PhotoImage(self.start_bg_image.resize((1600, 850), Image.Resampling.LANCZOS))
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.start_bg_photo)

        self.score = 0
        self.num_questions = 0
        self.total_questions = 10
        self.time_left = 90

        # UI ส่วนเกม
        self.game_frame = tk.Frame(self.root, bg="#7fd1d1", bd=10, relief="groove")
        self.game_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        self.question_label = tk.Label(
            self.root, text="", font=("Comic Sans MS", 20, "bold"), bg="#ffffff", fg="#ff5396"
        )
        self.question_label.place(relx=0.5, rely=0.3
, anchor="center")

        self.answer_entry = tk.Entry(self.root, font=("Comic Sans MS", 18), width=10)
        self.answer_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.answer_entry.bind("<Return>", self.check_answer)
        
        self.check_button = tk.Button(
            self.root,
            text="ตรวจสอบ",
            font=("Comic Sans MS", 18, "bold"),
            bg="#ff5396",
            fg="white",
            command=self.check_answer,
        )
        self.check_button.place(relx=0.5, rely=0.55, anchor="center")

        self.score_label = tk.Label(
            self.root, text="คะแนน: 0", font=("Comic Sans MS", 16), bg="#7fd1d1", fg="#cf007f"
        )
        self.score_label.place(relx=0.5, rely=0.65, anchor="center")

        self.timer_label = tk.Label(
            self.root,
            text="เวลา: 1 นาที 30 วินาที",
            font=("Comic Sans MS", 16),
            bg="#7fd1d1",
            fg="#cf007f",
        )
        self.timer_label.place(relx=0.5, rely=0.7, anchor="center")

        self.generate_question()
        self.start_timer()

    def generate_question(self):
        """สร้างคำถามใหม่"""
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operation = random.choice(["+", "-", "*", "/"])

        if operation == "/":
            while num2 == 0:
                num2 = random.randint(1, 20)
            num1 = num1 * num2
            self.answer = round(num1 / num2, 2)
        elif operation == "+":
            self.answer = num1 + num2
        elif operation == "-":
            self.answer = num1 - num2
        elif operation == "*":
            self.answer = num1 * num2

        self.question_label.config(text=f"{num1} {operation} {num2} = ?")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()

    def check_answer(self, event=None):
        """ตรวจสอบคำตอบ"""
        user_answer = self.answer_entry.get()
        try:
            user_answer = float(user_answer)
        except ValueError:
            messagebox.showerror("ผิดพลาด", "โปรดป้อนตัวเลขเท่านั้น")
            return

        if math.isclose(user_answer, self.answer, rel_tol=1e-5):
            self.score += 1
            messagebox.showinfo("ถูกต้อง", "คำตอบถูกต้อง!")
        else:
            messagebox.showerror("ผิดพลาด", f"คำตอบที่ถูกคือ {self.answer}")

        self.num_questions += 1
        self.score_label.config(text=f"คะแนน: {self.score}")

        if self.num_questions >= self.total_questions:
            self.end_game()
        else:
            self.generate_question()

    def start_timer(self):
        """เริ่มจับเวลา"""
        if self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f"เวลา: {minutes} นาที {seconds} วินาที")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            self.end_game()

    def end_game(self):
        """จบเกม"""
        feedback = "เก่งมาก!" if self.score >= 7 else "พยายามอีกครั้ง!"
        messagebox.showinfo(
            "จบเกม", f"คะแนนของคุณคือ {self.score}/{self.total_questions}\n{feedback}"
        )
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathGameWithCustomBackground(root)
    root.mainloop()
