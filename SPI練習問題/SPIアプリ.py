
import tkinter as tk
import pandas as pd
import random
from tkinter import messagebox, ttk



class SPIApp:

    def __init__(self, master):

        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("1200x800")

        # CSV読み込み　ヘッダーなし
        self.data = pd.read_csv('SPI試験問題と回答集_updated.csv', skiprows=1, header=None)

        #読み込んだファイルの列情報を設定
        self.data.columns = ["Category", "QuestionNo", "Question", "Choices", "Answer", "Advice"]


        #ランダムに70問抜き出し（重複しないように）
        self.questions = self.data.sample(70)
        self.current_question = -1

        # 得点の初期値
        self.score = 0

        # カウントダウンタイマー（60秒×70回）
        self.time_left = 60 * 70  # 70 minutes

        #canvasとscrollbarを設定
        self.canvas = tk.Canvas(self.master)
        self.scrollbar = tk.Scrollbar(self.master, command=self.canvas.yview) #commandはスクロールしたときの動作を指定（canvas表示領域を垂直方向に変化させる）
        self.canvas.config(yscrollcommand=self.scrollbar.set)                  #スクロールバーの開始位置ト終了位置を指定
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)               #canvasを設置、残りの領域は領域を占領True
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)                           #スクロールバーの位置決め

        # canvasにフレーム用意
        self.master_frame = tk.Frame(self.canvas)
        self.left_frame = tk.Frame(self.master_frame, bd=2, relief='sunken', padx=10, pady=10)          #左側のフレーム
        self.right_frame = tk.Frame(self.master_frame, bd=2, relief='sunken', padx=10, pady=10)         #右側のフレーム
        self.canvas.create_window((0,0), window=self.master_frame, anchor='nw')                         #Canvasに他のウィジェットを表示.create_window(座標, オプション) 　左上端に表示

        #canvas設定後にスクロールエリアを更新
        self.master_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        #問題番号リスト、問題番号一覧を作成
        self.question_list = tk.Listbox(self.left_frame, width=5, font=('Arial', 18), bd=2, relief='sunken')        #左側の問題リストに設定
        for i in range(1, len(self.questions) + 1):             #抽出した問題の数だけ繰り返す
            self.question_list.insert(tk.END, "Q{}".format(i))  #テキストボックスEntryに文字列Qをセットして問題番号表示

        #ウィジェットの用意
        self.score_label = tk.Label(self.right_frame, text="Score: 0", font=('Arial', 20))                                          #得点label
        self.timer_label = tk.Label(self.right_frame, text="残り時間: 70:00", font=('Arial', 20))                                  #タイマー
        self.question_label = tk.Label(self.right_frame, text="", wraplength=900, font=('Arial', 16), justify='left')               #設問
        self.choices = tk.Text(self.right_frame, wrap="word", font=('Arial', 14), relief='sunken', bd=2, padx=5, pady=5, width=80, height=10)           #ラベルの文字列が自動的に改行されるサイズを設定
        self.submit_button = tk.Button(self.right_frame, text="Submit Answer", command=self.check_answer, font=('Arial', 16), relief='raised', bd=2, padx=10, pady=5)   #回答提出ボタン
        self.answer_entry = tk.Entry(self.right_frame, font=('Arial', 16))      #回答入力ボックス


        #フレームを上から順に配置
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ウィジェットを上から順に配置
        self.question_list.pack(fill=tk.BOTH, expand=True)                      #問題リスト
        self.score_label.pack(padx=5, pady=5)#得点ラベル
        self.timer_label.pack(padx=5, pady=5)#タイマー
        self.question_label.pack(padx=5, pady=5)#問題ラベル
        self.choices.pack(padx=5, pady=5)

        self.answer_entry.pack(padx=5, pady=5)#回答入力
        self.submit_button.pack(padx=5, pady=5)#解答提出ボタン

        #クイズ更新
        self.next_question()

        #タイマー更新
        self.update_timer()

    #問題更新
    def next_question(self):
        self.current_question += 1          #インデックス
        if self.current_question < len(self.questions): #問題番号が抽出した問題数より小さいとき
            q = self.questions.iloc[self.current_question] #データを抽出して代入
            self.question_label.config(text=f"Question {self.current_question + 1}: {q['Question']}")       #問題ラベルの設定
            self.choices.delete(1.0, tk.END)
            self.choices.insert(tk.END, q["Choices"])                                                       #テキストボックスEntryに文字列Qを入力
            self.question_list.selection_clear(0, tk.END)
            self.question_list.selection_set(self.current_question)

        else:                   #問題番号が抽出した問題数と等しくなったときクイズ終了ダイアログ
            messagebox.showinfo("Quiz Finished", "You have finished the quiz. Your score is {}.".format(self.score))

    #回答チェック
    def check_answer(self):
        answer = self.answer_entry.get()#getメソッドで入力を受け取る
        correct_answer = self.questions.iloc[self.current_question]["Answer"].split("：")[1][0]

        #正解のとき
        if answer == correct_answer:
            self.score += 1     #得点加算
            self.score_label.config(text="Score: {}".format(self.score))        #スコアラベルの設定
            messagebox.showinfo("Correct", "Your answer is correct.\n" +            #messageboxで正解ダイアログ表示
                                self.questions.iloc[self.current_question]["Answer"] + "\n" +     #csvから作成したリストの解答とアドバイスを組み合わせて表示
                                self.questions.iloc[self.current_question]["Advice"])


        #不正解のとき
        else:
            messagebox.showinfo("Incorrect", "Your answer is incorrect.\n"+
                                self.questions.iloc[self.current_question]["Answer"] + "\n" +
                                self.questions.iloc[self.current_question]["Advice"])

        self.answer_entry.delete(0, tk.END)         #回答入力テキストボックスの文字を削除（削除開始位置、削除終了位置）
        self.next_question()     #問題更新

    #カウントダウン
    def update_timer(self):
        minutes = self.time_left // 60          #分表示
        seconds = self.time_left % 60           #秒表示
        self.timer_label.config(text="残り時間: {:02}:{:02}".format(minutes, seconds))
        self.time_left -= 1          #-1ずつカウントダウン
        #0以上のとき
        if self.time_left >= 0:
            self.master.after(1000, self.update_timer) #1000ms後にタイマー更新処理

        else:
            messagebox.showinfo("Time Up", "Time's up. You've scored {} points.".format(self.score))


#メインウィンドウ設定
root = tk.Tk()

#オブジェクト生成
app = SPIApp(root)

#メインループ
root.mainloop()
