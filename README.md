# AI To-Do List Manager

An AI-powered to-do list manager built with **Flask** and **Google Gemini API**.
You can add tasks with deadlines, mark them complete, delete completed tasks, and generate AI-based plain-text reports for any task.

## Features

* **Add Tasks** with deadlines.
* **Mark as Completed** and delete completed tasks.
* **AI Report Generation** for tasks using Google Gemini.
* Simple, clean web interface.

## Requirements

* Python 3.8+
* Flask
* google-generativeai

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-todo-list.git
   cd ai-todo-list
   ```
2. Install dependencies:

   ```bash
   pip install flask google-generativeai
   ```
3. Add your **Google API Key** in the code:

   ```python
   genai.configure(api_key="YOUR_API_KEY")
   ```
4. Run the app:

   ```bash
   python app.py
   ```
5. Open in your browser:

   ```
   http://127.0.0.1:8000
   ```

## File Structure

```
app.py          # Main Flask app  
tasks.json      # Stores tasks  
README.md       # Project info  
```
## License
This project is licensed under the MIT License.

