import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from progress import process_video, generate_speech, merge_video_and_audio
import os
import webbrowser

def show_final_output_screen(video_path):
    final_output_screen = tk.Toplevel()
    final_output_screen.title("Final Output")
    final_output_screen.geometry("600x400")
    
    tk.Label(final_output_screen, text="Final Output Video").pack(pady=20)
    
    if os.path.exists(video_path):
        video_label = tk.Label(final_output_screen, text=f"Final video saved at: {video_path}")
        video_label.pack(pady=10)
        # Open video with default system player
        def play_video():
            webbrowser.open(video_path)
        
        tk.Button(final_output_screen, text="Play Video", command=play_video).pack(pady=20)
    else:
        tk.Label(final_output_screen, text="Error: Final video not found.").pack(pady=20)
    
    final_output_screen.mainloop()

def process_video_wrapper():
    video_path = video_file_path.get()
    input_lang = input_language.get()
    target_lang = target_language.get()
    
    if not video_path or not input_lang or not target_lang:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    
    video_file, text_chunks = process_video(video_path, input_language=input_lang, target_language=target_lang)
    
    if text_chunks:
        show_translated_text(text_chunks, video_file)
    
def show_translated_text(text_chunks, video_file):
    text_window = tk.Toplevel()
    text_window.title("Edit Translated Text")
    text_window.geometry("600x400")

    text_vars = []
    for i, text_chunk in enumerate(text_chunks):
        tk.Label(text_window, text=f"Chunk {i + 1}").pack(pady=5)
        text_var = tk.StringVar(value=text_chunk)
        text_vars.append(text_var)
        tk.Entry(text_window, textvariable=text_var, width=80).pack(pady=5)

    def on_save():
        modified_text_chunks = [text_var.get() for text_var in text_vars]
        audio_chunks = [f"chunk{i}.wav" for i in range(len(modified_text_chunks))]
        combined_audio_path = generate_speech(modified_text_chunks, audio_chunks)
        final_video_path = merge_video_and_audio(video_file, combined_audio_path)
        show_final_output_screen(final_video_path)
        text_window.destroy()
    
    tk.Button(text_window, text="Save and Generate Video", command=on_save).pack(pady=20)
    text_window.mainloop()

def open_user_input_screen():
    main_screen.destroy()
    user_input_screen()

def user_input_screen():
    global user_input_screen
    user_input_screen = tk.Tk()
    user_input_screen.title("Emotibridge - Input")
    user_input_screen.geometry("600x600")

    tk.Label(user_input_screen, text="Select Video File").pack(pady=10)
    global video_file_path
    video_file_path = tk.Entry(user_input_screen, width=50)
    video_file_path.pack(pady=5)
    tk.Button(user_input_screen, text="Browse", command=lambda: video_file_path.insert(0, filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")]))).pack(pady=5)

    tk.Label(user_input_screen, text="Input Language").pack(pady=10)
    global input_language
    input_language = ttk.Combobox(user_input_screen, values=["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh", "hu", "ko", "ja", "hi"])
    input_language.pack(pady=5)

    tk.Label(user_input_screen, text="Target Language").pack(pady=10)
    global target_language
    target_language = ttk.Combobox(user_input_screen, values=["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh", "hu", "ko", "ja", "hi"])
    target_language.pack(pady=5)

    tk.Button(user_input_screen, text="Process Video", command=process_video_wrapper).pack(pady=20)
    
    user_input_screen.mainloop()

# Main application screen
main_screen = tk.Tk()
main_screen.title("Emotibridge")
main_screen.geometry("300x200")

tk.Label(main_screen, text="Welcome to Emotibridge").pack(pady=20)
tk.Button(main_screen, text="Start", command=open_user_input_screen).pack(pady=20)

main_screen.mainloop()


