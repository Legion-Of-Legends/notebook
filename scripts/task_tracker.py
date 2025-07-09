import os
import datetime as dt

with open("../Tasks/README.md") as f:
    task_tracker = f.read()

# filter data
task_time = dt.datetime.strptime(task_tracker.split("## Date:")[1].strip().split("\n")[0].strip(), "%d %B, %Y").date()
task_date = task_time.day
task_month = task_time.month
task_year = task_time.year
next_day = task_time + dt.timedelta(days=1)

member_data_all = task_tracker.split("\n")[2:]
member_data = {}
count = 0
while count < len(member_data_all):
    if member_data_all[count].startswith("##"):
        member_name = member_data_all[count].split("##")[1].strip()
        member_task={}
        for i in range(count + 1, len(member_data_all)):
            if member_data_all[i].startswith("##"):
                break
            elif member_data_all[i].startswith("|--") or member_data_all[i].startswith("|Tasks ") or member_data_all[i].strip() == "":
                continue
            else:
                task = member_data_all[i].strip().split("|")
                member_task[task[1].strip()] = (True if task[2].strip().lower() == "yes" else False)
                # member_task[task[0].strip()] = task[1].strip()
        member_data[member_name] = member_task
    count += 1

print(member_data)
# Create directory for reports if it doesn't exist
file_route = f"../Reports/{task_year}/{task_time.strftime("%B")}.md"
os.makedirs(os.path.dirname(file_route), exist_ok=True)

with open(file_route, "w") as f:
    f.write(f"# Task Tracker Report for {task_time.strftime('%B %Y')}\n\n")
    table_data = """
    <table>
    <thead>
    <tr>
        <th>Member</th>
        <th>Task</th>
        <th>Total Days</th>
        <th>Completed</th>
        <th>Incompleted</th>
    </tr>
    </thead>\n
    <tbody>
    """
    for member, tasks in member_data.items():
        taskbody = ""
        task_count = 0
        for task, completed in tasks.items():
            if task_count == 0:
                taskbody += f"""
                <tr>
                <td rowspan="{len(tasks)}">{member}</td>
                <td>{task}</td>
                <td>Total</td>
                <td>{'Yes' if completed else 'No'}</td>
                <td>{'No' if completed else 'Yes'}</td></tr>\n
                """
                task_count += 1
                continue
            taskbody += f"""
            <tr>
            <td>{task}</td>
            <td>Total</td>
            <td>{'Yes' if completed else 'No'}</td>
            <td>{'No' if completed else 'Yes'}</td>
            </tr>\n
            """
            task_count += 1
        table_data += taskbody
    table_data += """
        </tbody>
        </table>
        """
    f.write(table_data)

