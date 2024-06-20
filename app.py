import customtkinter as ctk
import threading
from queue import Queue
import os

from question_service import QuestionService
from utils import synthesize_audio, autoplay_audio, make_recording, transcribe_audio

question_service = QuestionService()
BASE_URL = "https://8111-35-240-132-251.ngrok-free.app/"

class App:

    def __init__(self, root):
        self.root = root
        self.is_running = threading.Event()
        self.is_attempting = threading.Event()

    
        
        # Left Hud
        self.top_sub = ctk.CTkLabel(master=self.root,width=50,height=50,corner_radius=20,fg_color="#999")
        self.top_sub.grid(row=0, column=0, padx=(150,0), pady=(50,40),sticky="ns")
        
        self.top_sub_label_1 = ctk.CTkLabel(master=self.top_sub,width=300,height=80,corner_radius=0,fg_color="#ccc")
        self.top_sub_label_1.grid(row=0, column=0, padx=0, pady=(0, 0),sticky="n")
        self.top_sub_label_1.configure(text="Stats")
        
        self.top_sub_label_2 = ctk.CTkLabel(master=self.top_sub,width=300,height=120,corner_radius=0,fg_color="#ddd")
        self.top_sub_label_2.grid(row=1, column=0, padx=0, pady=(0, 0))
        self.top_sub_label_2.configure(text="Total Rounds")

        self.top_sub_label_3 = ctk.CTkLabel(master=self.top_sub,width=300,height=120,corner_radius=0,fg_color="#ddd")
        self.top_sub_label_3.grid(row=2, column=0, padx=0, pady=(0, 0))
        self.top_sub_label_3.configure(text="Score")
        
        self.top_sub_label_4 = ctk.CTkLabel(master=self.top_sub,width=300,height=120,corner_radius=0,fg_color="#ddd")
        self.top_sub_label_4.grid(row=3, column=0, padx=0, pady=(0, 0))
        self.top_sub_label_4.configure(text="Team1: 0 Team2: 0")
        

        # Right Hud
        self.top_sub1 = ctk.CTkLabel(master=self.root,width=800,height=400,corner_radius=20,fg_color="#fff")
        self.top_sub1.grid(row=0, column=1, padx=(0,10), pady=(50,40),sticky="we")
        

        self.start_button = ctk.CTkButton(master=root, text="Start Assessment", command=self.start_assessment)
        self.start_button.grid(row=3, column=1, padx=(0,300), pady=(0, 50))

        self.answer_button = ctk.CTkButton(master=root, text="Make Attempt", command=self.make_attempt)
        self.answer_button.grid(row=4, column=1, padx=(0,300), pady=(0, 0))

        self.spinner_label = ctk.CTkLabel(master=self.top_sub1, text_color="green",width=50,height=20,bg_color="#fff")
        self.spinner_label.configure(text="Assessment Ongoing...")
        self.spinner_label.grid_forget()  # Hide the spinner initially

        self.processing_answer_label = ctk.CTkLabel(master=self.top_sub1,width=50,height=20, text_color="blue",bg_color="#fff")
        self.processing_answer_label.grid(row=3, column=0, padx=0, pady=(0, 0))
        self.processing_answer_label.grid_forget()

        self.riddle_label = ctk.CTkLabel(master=self.top_sub1,width=200,height=40,bg_color="#fff")
        self.riddle_label.grid(row=0, column=0, padx=(0,600), pady=(0, 0),sticky='n')
        self.riddle_label.configure(text="Round:")
        
        self.other_teams_scores = ctk.CTkLabel(master=self.top_sub1,width=800,height=40,fg_color="#fff")
        self.other_teams_scores.grid(row=1, column=0, padx=(0,0), pady=(0,0),sticky='n')
        self.other_teams_scores.configure(text=f"Your input:")
        


        self.worker_thread = None
        self.current_question = "None"
        self.score = 0
        self.audio_queue = Queue()
        
        # Current Question and answers
        self.current_answer = []
        self.current_question_object = {}

        self.remaining_clues = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_labels(self):
        self.riddle_label.configure(text=f"Question: {self.current_question}")
        self.top_sub_label_3.configure(text=f"Score: {self.score}")

    def start_assessment(self):
        if self.worker_thread and self.worker_thread.is_alive():
            # Assessment is already running.
            return

        self.spinner_label.grid(row=0, column=0, padx=0, pady=(10,0),sticky="n")  # Show the spinner
        self.worker_thread = threading.Thread(target=self.assessment_simulation)
        self.worker_thread.start()
        self.start_button.configure(text="Next Riddle")

    def assessment_simulation(self):
        self.process_questions()
        self.spinner_label.grid_forget()  # Hide the spinner after assessment is done

    def process_questions(self):
        self.update_labels()
    
        # if self.current_riddle_id == 1:
        #     autoplay_audio(audio_path="cache/round_rules.wav")
        
        #autoplay_audio(audio_path=f"cache/riddle_{self.current_riddle_id}.wav")
        question = question_service.get_next_question(self.current_answer)
        self.current_question_object = question
        self.current_answer.append(question)

        
        question_audio = synthesize_audio(question['question'])
        self.is_running.set()  # Allow processing for the new riddle
    
        while True:
            # clue_audio_path = synthesize_audio(text=clue.strip().lower(), base_url=BASE_URL)
            # print(f"Processing Clue {clue_num}")
            autoplay_audio(audio_path=question_audio)

            # Prefetch the next clue's audio if it exists
            #if clue_num < len(clues):
            #    threading.Thread(target=self.synthesize_and_queue_audio, args=(clues[clue_num].strip(),)).start()

            # Check if the user wants to make an attempt
            if self.is_attempting.is_set():
                self.handle_attempt()
                self.is_attempting.clear()
                break

        self.is_running.clear()
        if not self.is_attempting.is_set():  # If an attempt was not made, move to the next riddle
            self.go_to_next_question()

    def synthesize_and_queue_audio(self, text):
        clue_audio_path = synthesize_audio(text=text, base_url=BASE_URL)
        self.audio_queue.put(clue_audio_path)

    def make_attempt(self):
        if self.is_running.is_set():
            self.is_attempting.set()

    def handle_attempt(self):
        if self.current_question["time"]:
            self.processing_answer_label.configure(text=f"Recording Answer. You have 5 seconds to provide your answer...")
            self.processing_answer_label.pack(pady=20)  # Show the processing label
        
        answer_audio_path = make_recording()
        autoplay_audio(answer_audio_path)
        
        self.processing_answer_label.configure(text="Processing Your Answer...")
        user_answer = transcribe_audio(audio_path=answer_audio_path, base_url=BASE_URL)
        # Update current user answer
        self.current_answer = user_answer
        
        self.current_question = question_service.get_next_question(self.current_answer)
        
        if self.current_question_object['quiz_mistress_remarks'] == 'That is Correct':
            autoplay_audio(audio_path="./cache/correct.wav")
            # if clue_num == 1:
            #     self.score += 5
            #     annon_audio_path = synthesize_audio(text="I was on the first clue, five points.", base_url=BASE_URL)
            #     autoplay_audio(annon_audio_path)
            # elif clue_num == 2:
            #     self.score += 4
            #     annon_audio_path = synthesize_audio(text="I was on the second clue, four points.", base_url=BASE_URL)
            #     autoplay_audio(annon_audio_path)
            # else:
            #     self.score += 3
            #     if clue_num == 3:
            #         suffix = "rd"
            #     else:
            #         suffix = "th"
            #         annon_audio_path = synthesize_audio(text=f"I was on the {clue_num}{suffix} clue, three points.", base_url=BASE_URL)
            #     autoplay_audio(annon_audio_path)
        else:
            autoplay_audio(audio_path="./cache/incorrect.wav")
        self.update_labels()
        self.processing_answer_label.pack_forget()  # Hide the processing label
        self.go_to_next_question()

    def go_to_next_question(self):
            self.start_assessment()  # Start the assessment for the next question
            self.start_button.configure(text="Start Assessment")

    def on_closing(self):
        self.root.destroy()
        os._exit(0)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x1000")
    app = App(root)
    root.mainloop()
