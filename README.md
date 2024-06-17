# NSMQ_GYM by SASEK LABS


## Installation and Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/TechtenPlanet/AfricAIED_SASEK
    cd your-repo-name
    ```

2. **Create a Virtual Environment:**

    First, cd into the project directory: 
    ```bash
    cd AfricAIED_SASEK
    ```

    On macOS and Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application


1. Download the "AI Voice Models" folder onto your pc from [here](https://drive.google.com/drive/folders/1fr5uPj9NOVq8L2gws_DQCLvRRvmUhlY2)


2. Upload the extracted version of the zip that will be downloaded onto your pc into your google drive

 !["Google Drive"](/screenshots/google_drive.png)



3. Create and Ngrok account and get an API key. Ngrok will help you connect to the backend of this program. 


    
1. **Run the Server Notebook:**

    1. Upload the Server Notebook file to colab. Click on file and then click on upload notebook. Use any of 
       the methods available to upload your notebook file.

    2. 

    1. In google colab, make sure you copy the path to the quizmistress.json and quizmistress.onnx files that you
       uploaded to your google drive and replace these paths in the Riddle Prep App Server.ipynb file.

       ```
       # Load TTS model
       live_config=VitsConfig()
       live_config.load_json("/replace_the_path/you/will/findhere_with/the_correct_one.json")
       live_vits = Vits.init_from_config(live_config)
       live_vits.load_onnx("/replace_the_path/you/will/findhere_with/the_correct_one.onnx")

       clear_output()
       ```

    Make sure to move quizmistress.pth into the content folder in google colab.

    Open the `[Release] Riddle Prep App Server.ipynb` file, preferably in Colab if you don't have a GPU on your, follow the instructions to start the server, and copy the `ngrok` URL.

2. **Update `app.py`:**

    Paste the `ngrok` URL into the `BASE_URL` variable at the top of the `app.py` file.

3. **Run `app.py`:**

    ```bash
    python app.py
    ```
