import csv
import random
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import math

file_path = ""


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

    random.shuffle(names)

    teams = []
    i = 0

    for s in sizes:
        teams.append(names[i:i+s])
        i += s

    return teams


# -----------------------------
# CSV 읽기
# -----------------------------
def load_csv(path):

    paper = []
    wargame = []

    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for row in reader:

            if len(row) < 2:
                continue

            name = row[0].strip()
            field = row[1].strip()

            if field == "논문":
                paper.append(name)

            elif field == "워게임":
                wargame.append(name)

    return paper, wargame


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

    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files","*.csv")]
    )

    file_label.config(text=file_path)


# -----------------------------
# 팀 생성 실행
# -----------------------------
def run_program():

    if file_path == "":
        messagebox.showerror("오류","CSV 파일 선택하세요")
        return

    seed_value = int(time.time())
    random.seed(seed_value)

    result_box.delete("1.0",tk.END)
    result_box.insert(tk.END,f"랜덤 시드: {seed_value}\n\n")

    paper, wargame = load_csv(file_path)

    paper_teams = make_teams(paper)
    wargame_teams = make_teams(wargame)

    result_rows = []

    result_box.insert(tk.END,"===== 논문 팀 =====\n")

    for i,team in enumerate(paper_teams,1):

        team_name = f"논문{i}팀"

        result_box.insert(tk.END,team_name+" : "+", ".join(team)+"\n")

        for name in team:
            result_rows.append([name,"논문",team_name])

    result_box.insert(tk.END,"\n===== 워게임 팀 =====\n")

    for i,team in enumerate(wargame_teams,1):

        team_name = f"워게임{i}팀"

        result_box.insert(tk.END,team_name+" : "+", ".join(team)+"\n")

        for name in team:
            result_rows.append([name,"워게임",team_name])


    # 출력 파일 생성
    output_file = generate_output_filename(file_path)

    with open(output_file,"w",newline='',encoding="utf-8-sig") as f:

        writer = csv.writer(f)
        writer.writerow(["이름","분야","팀명"])
        writer.writerows(result_rows)


    result_box.insert(tk.END,f"\n{output_file} 저장 완료")


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("랜덤 팀 생성기")
root.geometry("600x500")

title = tk.Label(root,text="랜덤 팀 생성기",font=("Arial",16))
title.pack(pady=10)

btn_file = tk.Button(root,text="CSV 파일 선택",command=choose_file)
btn_file.pack()

file_label = tk.Label(root,text="선택된 파일 없음")
file_label.pack(pady=5)

btn_run = tk.Button(root,text="팀 생성",command=run_program)
btn_run.pack(pady=10)

result_box = tk.Text(root,height=20,width=70)
result_box.pack()

root.mainloop()
