import streamlit as st

st.set_page_config(page_title="To-Do App", page_icon="📝")

st.title("📝 To-Do List Application")

# Initialize memory for tasks
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

# Text box for adding new task
st.subheader("➕ Add a Task")

new_task = st.text_input("Enter a new task:", placeholder="e.g., Buy groceries")

if st.button("Add Task"):
    if new_task.strip() != "":
        st.session_state["tasks"].append({"task": new_task, "completed": False})
        st.success("Task added!")
    else:
        st.warning("Please enter a task.")

st.divider()

# Display tasks
st.subheader("📋 Your Tasks")

if len(st.session_state["tasks"]) == 0:
    st.info("No tasks yet. Add one above 👆")
else:
    # Show each task
    for i, t in enumerate(st.session_state["tasks"]):
        col1, col2, col3 = st.columns([4,1,1])

        with col1:
            if t["completed"]:
                st.write(f"✔️ ~~{t['task']}~~")
            else:
                st.write(f"🔹 {t['task']}")

        # Mark task as completed
        with col2:
            if st.button("Done", key=f"done_{i}"):
                st.session_state["tasks"][i]["completed"] = True

        # Delete task
        with col3:
            if st.button("❌", key=f"delete_{i}"):
                st.session_state["tasks"].pop(i)
                st.rerun()

st.divider()

# Clear all tasks
if len(st.session_state["tasks"]) > 0:
    if st.button("Clear All Tasks"):
        st.session_state["tasks"] = []
        st.success("All tasks cleared!")
