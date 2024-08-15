import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, DND_TEXT, TkinterDnD

class HebrewKeyboardConverter:
    def __init__(self):
        self.english_to_hebrew = {
            'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
            'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך',
            'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ',
            ',': 'ת', '.': 'ץ', ';': 'ף', "'": ',', '/': '.'
        }

    def convert(self, text):
        return ''.join(self.english_to_hebrew.get(char.lower(), char) for char in text)

class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.converter = HebrewKeyboardConverter()
        self.title("Hebrew Keyboard Layout Converter")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.text_input = tk.Text(self, height=10, wrap=tk.WORD)
        self.text_input.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_input.bind('<KeyRelease>', self.on_key_release)
        self.text_input.insert("1.0", "Drag and drop text or a file here")
        self.text_input.config(fg='grey')
        self.text_input.bind("<FocusIn>", self.on_focus_in)
        self.text_input.bind("<FocusOut>", self.on_focus_out)
        self.text_input.tag_configure("right", justify='right')
        self.text_input.tag_add("right", "1.0", "end")

        self.text_input.drop_target_register(DND_FILES, DND_TEXT)
        self.text_input.dnd_bind('<<Drop>>', self.drop)

        self.text_output = tk.Text(self, height=10, wrap=tk.WORD)
        self.text_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_output.tag_configure("right", justify='right')

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        load_button = tk.Button(button_frame, text="Load File", command=self.load_file, 
                                bg='#4CAF50', fg='white', padx=20, pady=10, font=('Arial', 12))
        load_button.pack(side=tk.LEFT, padx=10)

        paste_button = tk.Button(button_frame, text="Paste", command=self.paste_text,
                                 bg='#2196F3', fg='white', padx=20, pady=10, font=('Arial', 12))
        paste_button.pack(side=tk.LEFT, padx=10)

    def on_focus_in(self, event):
        if self.text_input.get("1.0", tk.END).strip() == "Drag and drop text or a file here":
            self.text_input.delete("1.0", tk.END)
            self.text_input.config(fg='black')

    def on_focus_out(self, event):
        if not self.text_input.get("1.0", tk.END).strip():
            self.text_input.insert("1.0", "Drag and drop text or a file here")
            self.text_input.config(fg='grey')
        self.text_input.tag_add("right", "1.0", "end")

    def on_key_release(self, event):
        self.convert_text()

    def convert_text(self):
        input_text = self.text_input.get("1.0", tk.END)
        converted_text = self.converter.convert(input_text)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, converted_text)
        self.text_output.tag_add("right", "1.0", "end")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.load_file_content(file_path)

    def load_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, content)
            self.text_input.tag_add("right", "1.0", "end")
            self.convert_text()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def paste_text(self):
        try:
            clipboard_text = self.clipboard_get()
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, clipboard_text)
            self.text_input.tag_add("right", "1.0", "end")
            self.convert_text()
        except tk.TclError:
            messagebox.showinfo("Info", "Clipboard is empty or contains non-text data.")

    def drop(self, event):
        if event.data.startswith('{'):
            # It's a file
            file_path = event.data.strip('{}')
            self.load_file_content(file_path)
        else:
            # It's text
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, event.data)
            self.text_input.tag_add("right", "1.0", "end")
            self.convert_text()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
