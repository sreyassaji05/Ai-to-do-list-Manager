from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import json
import os

app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key="enter your google api key")  # Replace with your actual Gemini API key

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
        print("Saving tasks:", tasks)

@app.route('/')
def home():
    tasks = load_tasks()
    tasks_html = ""
    for i, task in enumerate(tasks):
        checked = 'checked' if task.get('completed') else ''
        tasks_html += f'''
        <div>
          <input type="checkbox" onchange="markCompleted({i}, this.checked)" {checked}>
          <p><strong>Task:</strong> {task['task']}</p>
          <p><strong>Deadline:</strong> {task['deadline']}</p>
          <button onclick="generate('{task['task']}', this)">Generate task</button>
          <textarea readonly placeholder="Generated report will appear here..."></textarea>
        </div>
        '''

    return render_template_string(HTML_TEMPLATE.replace("<!--TASKS-->", tasks_html))

@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data.get('task', '')
    deadline = data.get('deadline', '')
    tasks = load_tasks()
    tasks.append({"task": task, "deadline": deadline, "completed": False})
    save_tasks(tasks)
    return jsonify({"status": "saved"})

@app.route('/complete', methods=['POST'])
def complete_task():
    data = request.get_json()
    index = data.get('index')
    completed = data.get('completed')
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['completed'] = completed
        save_tasks(tasks)
    return jsonify({"status": "updated"})

@app.route('/delete-completed', methods=['POST'])
def delete_completed():
    tasks = load_tasks()
    tasks = [task for task in tasks if not task.get('completed')]
    save_tasks(tasks)
    return jsonify({"status": "deleted"})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"Write a plain text report without any markdown, HTML, or formatting symbols on: {prompt}")
        return jsonify({"text": response.text})
    except Exception as e:
        print("Error from Gemini API:", e)
        return jsonify({"text": "Error generating response."}), 500

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI To-Do List Manager</title>
  <style>
    h1 {
      text-align: center;
    }
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background-color: #d3d3d3; /* Darker grey background */
    }
    #taskForm, #taskList, button {
      width: 50%;
      margin: 10px 0;
      text-align: center;
    }
    #taskList div {
      border: 1px solid #ccc;
      padding: 10px;
      margin: 5px 0;
      border-radius: 5px;
      background-color: #f9f9f9; /* Light grey or white background for tasks */
      position: relative;
    }
    textarea {
      width: 100%;
      margin-top: 5px;
      resize: vertical; /* Allow resizing only vertically */
      max-height: 200px; /* Limit the maximum height */
      overflow: auto; /* Add scrollbars if content exceeds height */
    }
  </style>
</head>
<body>
  <h1>AI To-Do List Manager</h1>
  <form id="taskForm">
    <input type="text" id="taskInput" placeholder="Enter task" style="width: 70%;">
    <input type="datetime-local" id="deadlineInput" style="width: 70%;">
    <button type="submit">Add Task</button>
  </form>
  <button onclick="deleteCompletedTasks()">Delete Completed Tasks</button>
  <div id="taskList"><!--TASKS--></div>
  <script>
    const form = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');

    form.onsubmit = async (e) => {
      e.preventDefault();
      const task = document.getElementById('taskInput').value;
      const deadline = document.getElementById('deadlineInput').value;

      const response = await fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task, deadline })
      });

      if (response.ok) {
        location.reload();
      }
    }

    async function markCompleted(index, completed) {
      await fetch('/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index, completed })
      });
    }

    async function deleteCompletedTasks() {
      const response = await fetch('/delete-completed', {
        method: 'POST'
      });
      if (response.ok) {
        location.reload();
      }
    }

    async function generate(promptText, button) {
      const textarea = button.nextElementSibling;
      textarea.value = "Generating...";
      const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptText })
      });
      const data = await response.json();
      textarea.value = data.text || 'No response';
    }
  </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(port=8000, debug=True)

