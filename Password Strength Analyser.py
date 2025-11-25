import math
import re
import nltk
from nltk.corpus import words
import tkinter as tk
from tkinter import messagebox

common_words = set(w.lower() for w in words.words()) # load dictionary word list and converts it to lowercase

def in_dictionary(password, word_list):
    password_lower = password.lower() # converts password to lowercase to check for any real words against the dictionary
    for word in word_list:
        if word in password_lower and len(word) > 3:    # ignore very short words
            return True
    return False

def password_entropy(password):
    score = 0
    feedback = []

    if re.search(r"[a-z]", password):
        score += 26
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 26
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 10
    else:
        feedback.append("Include numbers.")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 32
    else:
        feedback.append("Include special characters.")

    entropy = len(password) * math.log2(score)  # calculates entropy

    if len(password) < 12:
        feedback.append("Make your password longer (12+ characters).") # length check

    if in_dictionary(password, common_words):   # removes score if dictionary word is found
        entropy -= 20
        feedback.append("Avoid using real words or common phrases.")

    if entropy < 28:
        strength = "Weak"
    elif entropy < 60:
        strength = "Medium"
    else:
        strength = "Strong"

    return entropy, strength, feedback


root = tk.Tk()  # gui setup
root.title("Password Strength Analyzer")

tk.Label(root, text="Enter a password:").pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

output_label = tk.Label(root, text="", justify="left", anchor="w")
output_label.pack(pady=10)

def check_password(event=None):  # event=None lets you bind Enter key too
    user_password = entry.get()
    entropy, strength, feedback = password_entropy(user_password)

    result = f"Entropy: {entropy:.2f} bits\nPassword Strength: {strength}\n"
    if not feedback:
        result += "No feedback needed - your password looks good!"
    else:
        result += "Feedback:\n" + "\n".join(f"- {f}" for f in feedback)

    output_label.config(text=result)

tk.Button(root, text="Check Strength", command=check_password).pack(pady=10)

root.bind('<Return>', check_password)

root.mainloop()