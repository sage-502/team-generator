import csv
import random
import time
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import math

file_path = ""
fields_data = {}
last_result = []
attempt_count = 0
result_text_cache = ""


# -----------------------------
# 균등 팀 분배 (3~5명)
# -----------------------------
def balanced_team_sizes(n):

    if n <= 5:
        return [n]

    team_count = math.ceil(n / 5)

    base = n // team_count
    remainder = n % team_count

    sizes = [base] * team_count

    for i in range(remainder):
        sizes[i] += 1

    return sizes


# -----------------------------
# 팀 생성
# -----------------------------
def make_teams(names):

    n = len(names)

    if n <= 5:
        return [names]

    sizes = balanced_team_sizes(n)

    shuffled = names[:]
    random.shuffle(shuffled)

    teams = []
    i = 0

    for s in sizes:
        teams.append(shuffled[i:i+s])
        i += s

    return teams


# -----------------------------
# CSV 읽기
# -----------------------------
def load_csv(path):

    fields = {}

    with open(path, newline='', encoding='utf-8-sig') as f:

        reader = csv.reader(f)

        for row in reader:

            if len(row) < 2:
                continue

            name = row[0].strip()
            field = row[1].strip()

            if field not in fields:
                fields[field] = []

            fields[field].append(name)

    return fields


# -----------------------------
# 출력 파일 이름 생성
# -----------------------------
def generate_output_filename(input_path):

    base = os.path.splitext(os.path.basename(input_path))[0]
    folder = os.path.dirname(input_path)

    output_file = os.path.join(folder, f"{base}(output).csv")

    if not os.path.exists(output_file):
        return output_file

    i = 2
    while True:

        output_file = os.path.join(folder, f"{base}(output{i}).csv")

        if not os.path.exists(output_file):
            return output_file

        i += 1


# -----------------------------
# 파일 선택
# -----------------------------
def choose_file():

    global file_path
    global fields_data
    global attempt_count

    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files","*.csv")]
    )

    if file_path:
        file_label.config(text=file_path)
        fields_data = load_csv(file_path)
        attempt_count = 0


# -----------------------------
# 팀 생성
# -----------------------------
def generate_teams():

    global last_result
    global attempt_count
    global result_text_cache

    if not fields_data:
        messagebox.showerror("오류","CSV 파일 먼저 선택하세요")
        return

    attempt_count += 1

    seed_value = int(time.time())
    random.seed(seed_value)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result_box.delete("1.0", tk.END)

    header = f"생성 시각: {now}\n랜덤 시드: {seed_value}\n시도 횟수: {attempt_count}\n\n"

    result_box.insert(tk.END, header)
    result_text_cache = header

    result_rows = []

    for field, names in fields_data.items():

        teams = make_teams(names)

        title = f"===== {field} 팀 =====\n"
        result_box.insert(tk.END, title)
        result_text_cache += title

        for i, team in enumerate(teams, 1):

            team_name = f"{field}{i}팀"

            line = team_name + " : " + ", ".join(team) + "\n"

            result_box.insert(tk.END, line)
            result_text_cache += line

            for name in team:
                result_rows.append([name, field, team_name])

        result_box.insert(tk.END, "\n")
        result_text_cache += "\n"

    last_result = result_rows


# -----------------------------
# 파일 저장
# -----------------------------
def save_file():

    if not last_result:
        messagebox.showerror("오류","먼저 팀을 생성하세요")
        return

    output_file = generate_output_filename(file_path)

    with open(output_file, "w", newline='', encoding="utf-8-sig") as f:

        writer = csv.writer(f)
        writer.writerow(["이름","분야","팀명"])
        writer.writerows(last_result)

    result_box.insert(tk.END, f"{output_file} 저장 완료\n")
    result_text_cache += f"{output_file} 저장 완료\n"


# -----------------------------
# 클립보드 복사
# -----------------------------
def copy_to_clipboard():

    if not result_text_cache:
        messagebox.showerror("오류","먼저 팀을 생성하세요")
        return

    root.clipboard_clear()
    root.clipboard_append(result_text_cache)
    root.update()

    messagebox.showinfo("복사 완료","팀 결과가 클립보드에 복사되었습니다")


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("랜덤 팀 생성기")
root.geometry("700x550")


# 파일 선택 영역
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

btn_file = tk.Button(top_frame,text="CSV 파일 선택",command=choose_file,width=15)
btn_file.pack(side="left", padx=5)

file_label = tk.Label(top_frame,text="선택된 파일 없음",anchor="w")
file_label.pack(side="left", padx=5)


# 버튼 영역
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

btn_generate = tk.Button(button_frame,text="팀 생성",width=12,command=generate_teams)
btn_generate.pack(side="left", padx=5)

btn_save = tk.Button(button_frame,text="파일 저장",width=12,command=save_file)
btn_save.pack(side="left", padx=5)

btn_copy = tk.Button(button_frame,text="결과 복사",width=12,command=copy_to_clipboard)
btn_copy.pack(side="left", padx=5)


# 구분선
separator = tk.Frame(root,height=2,bd=1,relief="sunken")
separator.pack(fill="x", padx=10, pady=10)


# 결과 출력 영역
result_frame = tk.Frame(root)
result_frame.pack(fill="both", expand=True, padx=10, pady=5)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(
    result_frame,
    yscrollcommand=scrollbar.set,
    wrap="word"
)

result_box.pack(fill="both", expand=True)

scrollbar.config(command=result_box.yview)


root.mainloop()
