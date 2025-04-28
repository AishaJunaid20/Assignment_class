import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# File path to store tasks
TASKS_FILE = 'tasks.json'

# Task class
class Task:
    def __init__(self, name, due_date, priority):
        self.name = name
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.priority = priority
        self.status = 'Pending'

    def mark_as_completed(self):
        self.status = 'Completed'

    def __str__(self):
        return f"{self.name} | {self.due_date.strftime('%Y-%m-%d')} | Priority: {self.priority} | Status: {self.status}"

    def to_dict(self):
        return {
            'Task': self.name,
            'Due Date': self.due_date.strftime('%Y-%m-%d'),
            'Priority': self.priority,
            'Status': self.status
        }

# TaskManager class
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                loaded_tasks = json.load(f)
                self.tasks = [Task(task['Task'], task['Due Date'], task['Priority']) for task in loaded_tasks]

    def save_tasks(self):
        """Save tasks to the JSON file."""
        with open(TASKS_FILE, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, task_name, due_date, priority):
        task = Task(task_name, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.name != task_name]
        self.save_tasks()

    def mark_as_completed(self, task_name):
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_completed()
        self.save_tasks()

    def get_all_tasks(self):
        return [task.to_dict() for task in self.tasks]

# Initialize TaskManager
task_manager = TaskManager()

# Streamlit page configuration
st.set_page_config(page_title="Task Manager", page_icon="📋", layout="wide")

# Styling for a better UI
st.markdown("""
    <style>
    .stButton>button {
        background-color: #008CBA;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 15em;
        margin: 10px;
    }
    .stTextInput>div>input {
        border-radius: 8px;
        height: 2.5em;
        font-size: 18px;
        width: 100%;
    }
    .stSelectbox>div>div>div {
        background-color: #f0f8ff;
        border-radius: 8px;
    }
    .stMarkdown {
        color: #333;
        font-family: 'Helvetica', sans-serif;
    }
    .stTable {
        background-color: #f4f4f9;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with emoji
st.title("Task Manager 📋")
st.markdown("Manage your tasks efficiently with deadlines and priorities.")

# Function to add a task
def add_task():
    task_name = st.text_input("Task Name", placeholder="Enter the task name")
    due_date = st.date_input("Due Date", min_value=datetime.today())
    priority = st.selectbox("Priority", ['Low', 'Medium', 'High'])
    
    if st.button("Add Task", key="add_task"):
        task_manager.add_task(task_name, due_date.strftime('%Y-%m-%d'), priority)
        st.success(f"Task **{task_name}** added successfully! 🎉")

# Function to display tasks in a table
def display_tasks():
    tasks = task_manager.get_all_tasks()
    if tasks:
        df = pd.DataFrame(tasks)
        st.dataframe(df, width=800)
    else:
        st.warning("No tasks available. Add some tasks! 😅")

# Function to mark task as completed
def mark_completed():
    tasks = task_manager.get_all_tasks()
    task_names = [task['Task'] for task in tasks]
    task_to_complete = st.selectbox("Select a task to mark as completed", task_names)
    if st.button("Mark as Completed", key="complete"):
        task_manager.mark_as_completed(task_to_complete)
        st.success(f"Task **{task_to_complete}** marked as completed! ✅")

# Function to delete a task
def delete_task():
    tasks = task_manager.get_all_tasks()
    task_names = [task['Task'] for task in tasks]
    task_to_delete = st.selectbox("Select a task to delete", task_names)
    if st.button("Delete Task", key="delete"):
        task_manager.delete_task(task_to_delete)
        st.success(f"Task **{task_to_delete}** deleted successfully! 🗑️")

# Sidebar navigation
st.sidebar.header("Task Manager Options")
option = st.sidebar.radio("Choose an action", ["Add Task", "View Tasks", "Mark Task as Completed", "Delete Task"])

# Main app interface
if option == "Add Task":
    add_task()
elif option == "View Tasks":
    display_tasks()
elif option == "Mark Task as Completed":
    mark_completed()
elif option == "Delete Task":
    delete_task()

# Footer with your name and emoji
st.markdown("### Developed by Aisha Junaid 💻")
st.markdown("**Task Manager** - A simple, interactive tool to manage your tasks with deadlines and priorities. 💡")
