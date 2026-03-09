import csv
import random
import time
import tkinter as tk
from tkinter import filedialog, messagebox

file_path = ""


# -----------------------------
# 팀 사이즈 조합 계산
# -----------------------------
def possible_team_sizes(n):

    results = []

    def dfs(remain, path):
        if remain == 0:
            results.append(path)
            return

        for s in [3,4,5]:
            if remain - s >= 0:
                dfs(remain-s, path+[s])

    dfs(n, [])
    return results


# -----------------------------
# 팀 생성
# -----------------------------
def make_teams(names):

    n = len(names)

    if n <= 5:
        return [names]

    options = possible_team_sizes(n)

    if not options:
        raise ValueError(f"{n}명은 팀 구성 불가")

    sizes = random.choice(options)

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


    # 결과 CSV 저장
    with open("output.csv","w",newline='',encoding="utf-8-sig") as f:

        writer = csv.writer(f)
        writer.writerow(["이름","분야","팀명"])

        writer.writerows(result_rows)

    result_box.insert(tk.END,"\noutput.csv 저장 완료")


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("랜덤 팀 생성기 (CSV 버전)")
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
