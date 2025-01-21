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
        self.root.resizable(True, True)

        # สีพื้นหลังระหว่างนับถอยหลัง
        self.bg_color = "#FFAFE0"

        # โหลดภาพพื้นหลังสำหรับเกม
        self.start_bg_image = Image.open("เกม คณิต คิด หรรษา.jpg")  # ภาพเริ่มต้น
       
        self.start_bg_photo = None
        self.game_bg_photo = None

        # สร้าง Canvas
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # ใส่พื้นหลังภาพเริ่มต้น
        self.start_bg_photo = ImageTk.PhotoImage(self.start_bg_image.resize((800, 600), Image.Resampling.LANCZOS))
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.start_bg_photo)

        # ปุ่มเริ่มเกม
        self.start_button = tk.Button(
            root,
            text="เริ่มเกม",
            font=("Comic Sans MS", 18, "bold"),
            bg="#FF69B4",
            fg="white",
            command=self.start_countdown,
        )
        self.start_button.place(relx=0.5, rely=0.8, anchor="center")

        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        """ปรับขนาดภาพพื้นหลังเมื่อหน้าต่างเปลี่ยนขนาด"""
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()

        if hasattr(self, "start_bg_photo") and self.start_bg_photo:
            resized_image = self.start_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.start_bg_photo = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.bg_item, image=self.start_bg_photo)

    def start_countdown(self):
        """เริ่มการนับถอยหลังก่อนเริ่มเกม"""
        self.start_button.destroy()  # ลบปุ่มเริ่มเกม

        # ตั้งค่าพื้นหลังสี
        self.canvas.config(bg=self.bg_color)
        self.canvas.delete("all")  # ลบภาพพื้นหลังเดิม

        self.label = tk.Label(
            self.root,
            text="เตรียมพร้อม!",
            font=("Comic Sans MS", 24, "bold"),
            bg=self.bg_color,
            fg="#FF1493",
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas.after(1000, lambda: self.update_countdown(3))

    def update_countdown(self, count):
        """อัปเดตตัวเลขนับถอยหลัง"""
        if count > 0:
            self.label.config(text=str(count))
            self.canvas.after(1000, lambda: self.update_countdown(count - 1))
        else:
            self.label.destroy()
            self.start_game()

    def start_game(self):
    # เปลี่ยนพื้นหลังเป็นภาพ math.jpg
        self.canvas.delete("all")
        self.bg_image = Image.open("math.jpg")
        self.bg_image = self.bg_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)  # ปรับขนาดให้เต็มหน้าต่าง
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.game_frame = tk.Frame(self.root, bg="#7fd1d1", bd=10, relief="groove")
        self.game_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        # ตั้งค่าเกม
        self.score = 0
        self.num_questions = 0
        self.total_questions = 10
        self.time_left = 90

        # UI ส่วนเกม
       
        self.question_label = tk.Label(
            self.root, text="", font=("Comic Sans MS", 20, "bold"), bg="#7fd1d1", fg="#ff5396"
        )
        self.question_label.place(relx=0.5, rely=0.3, anchor="center")

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
