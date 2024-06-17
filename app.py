import customtkinter as ctk
import threading
from queue import Queue
import os
from PIL import Image, ImageTk
from customtkinter import CTkImage
import threading
import time
from question_service import QuestionService
from utils import synthesize_audio, autoplay_audio, make_recording, transcribe_audio

question_service = QuestionService()
BASE_URL = "https://fe7f-34-143-171-208.ngrok-free.app/"


class App:

    def __init__(self, root):
        self.root = root
        self.thread = threading
        
        self.current_input = ""  # Set current input

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme(
            "blue"
        )  # Themes: "blue" (standard), "green", "dark-blue"

        img = Image.open("./images/nsmq.png")
        img = CTkImage(light_image=Image.open("./images/nsmq.png"), size=(60, 50))

        self.nsmq_image = ctk.CTkLabel(
            master=root, text=None, image=img, justify="left", anchor="w", width=250
        )
        self.nsmq_image.pack(pady=50)

        self.nsmq_image.place(x=23, y=26)

        self.top_frame = ctk.CTkFrame(
            master=self.root,
            # fg_color="light_color",
            width=900,
            height=800,
            corner_radius=25,
         
        )

        self.top_frame.pack(padx=180, pady=80,expand=True, fill="both")
        self.top_frame.configure(width=1200)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)

        self.sndFrame = ctk.CTkFrame(
            self.top_frame,
            height=300,
            corner_radius=25,
        )
        self.sndFrame.pack(padx=20, pady=10, expand=True, fill="both")
        self.sndFrame.place(x=0, y=0)
        self.team_points_label = ctk.CTkLabel(
            master=self.sndFrame, text=f"Team Points: 0", text_color="green"
        )
        

        self.question_label = ctk.CTkLabel(master=self.top_frame, text="Current question:")
        self.question_label.pack(padx=200, pady=30)

        self.score_label = ctk.CTkLabel(master=self.top_frame, text="Score: 0")
        self.score_label.pack(pady=30)

        self.user_input = ctk.CTkLabel(master=self.top_frame, text="Your input is: ")
        self.user_input.pack(pady=20)

        self.user_input_0 = ctk.CTkLabel(master=self.top_frame, text="")
        self.user_input_0.pack(pady=5)

        self.start_button = ctk.CTkButton(
            master=root, text="Start Assessment", command=self.start_assessment_thread
        )
        self.start_button.pack(pady=20)

        self.answer_button = ctk.CTkButton(
            master=root, text="Make Attempt", command=self.make_an_attempt
        )
        self.answer_button.pack(pady=20)

        self.spinner_label = ctk.CTkLabel(
            master=root, text="Assessment Ongoing...", text_color="green"
        )
        self.spinner_label.pack(pady=40)
        self.spinner_label.pack_forget()  # Hide the spinner initially

        self.processing_answer_label = ctk.CTkLabel(
            master=self.top_frame, text="", text_color="blue"
        )
        self.processing_answer_label.pack(pady=20)
        self.processing_answer_label.pack_forget()

        self.worker_thread = None
        self.current_riddle_id = 1
        self.score = 0
        self.audio_queue = Queue()

        self.memory = []
        self.started = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.attempted = False
        
    def update_memory(self,data):
        self.memory.append(data)
    
    def get_memory(self):
        return self.memory
    
    def update_score(self, score):
        self.score_label.config(text=f"Score: {score}")
    
    def update_input(self, input):
        self.current_input = input
        self.user_input_0.config(text=f"Your input: {input}")
        
    def update_current_question(self, current):
        self.question_label.config(text=f"Current question: {current} ")
        
    def start_assessment(self):
        response = question_service.get_next_question(self.memory)
        question_audio = synthesize_audio (response["question"])
        autoplay_audio(question_audio)
        time.sleep(response["time"])
        if self.attempted:
            return 
        else:
            self.update_memory("NO input")
            remark = question_service.get_next_question(self.memory)
            remark_audio = synthesize_audio(remark)
            autoplay_audio(remark_audio)
            
    def start_assessment_thread(self):
        if not self.started:
            autoplay_audio("./cache/round_rules.wav")
        threading.Thread(target=self.start_assessment).start()
        
    def make_an_attempt(self):
        self.attempted = True
        audio_path = make_recording()
        transcript = transcribe_audio(audio_path, BASE_URL)
        self.update_input(transcript)
        self.update_memory(transcript)
        response = question_service.get_next_question(self.memory)
        if response["remark"] == "correct":
            self.update_score(response["accumulated_points_for_team1"])

    
    def on_closing(self):
        self.root.destroy()
        os._exit(0)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("900x700")
    app = App(root)
    root.mainloop()
