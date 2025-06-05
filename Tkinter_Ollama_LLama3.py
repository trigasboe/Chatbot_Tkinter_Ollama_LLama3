import tkinter as tk
from tkinter import scrolledtext
import requests
import threading

def generate_answer():
    question = entry.get()
    if not question.strip():
        return

    status_label.config(text="⏳ Menjawab...", fg="orange")
    answer_area.config(state="normal")
    answer_area.insert(tk.END, f"\n🧑‍💬 Pertanyaan: {question}\n")
    answer_area.insert(tk.END, "🤖 Menjawab...\n")
    answer_area.config(state="disabled")
    answer_area.yview(tk.END)

    def ask_ollama():
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": f"Jelaskan dalam bahasa Indonesia: {question}",
                    "stream": False
                }
            )
            data = response.json()
            jawaban = data.get("response", "Tidak ada jawaban.")
            status_label.config(text="✅ Jawaban siap.", fg="green")
        except Exception as e:
            jawaban = f"(Kesalahan: {e})"
            status_label.config(text="❌ Gagal menjawab.", fg="red")

        answer_area.config(state="normal")
        answer_area.insert(tk.END, f"🤖 Jawaban: {jawaban}\n")
        answer_area.config(state="disabled")
        answer_area.yview(tk.END)

    threading.Thread(target=ask_ollama).start()

# === GUI setup ===
root = tk.Tk()
root.title("Asisten Lokal - Ollama + LLaMA3")
root.geometry("600x520")
root.configure(bg="#eef7ff")

title = tk.Label(root, text="Asisten Lokal (Ollama - LLaMA3)", font=("Arial", 16, "bold"), bg="#eef7ff", fg="#003366")
title.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=50, bd=2, relief="groove")
entry.pack(pady=10)
entry.focus()

submit_btn = tk.Button(root, text="Tanyakan", font=("Arial", 12, "bold"), bg="#3399ff", fg="white", command=generate_answer)
submit_btn.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 11, "italic"), bg="#eef7ff", fg="gray")
status_label.pack(pady=5)

answer_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state="disabled", width=70, height=15, bg="#f8fbff")
answer_area.pack(padx=10, pady=10)

root.mainloop()
