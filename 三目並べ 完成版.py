import random

#三目並べの座標をリストで表現
Board=[0,1,2,3,4,5,6,7,8]

#座標の表示間隔
a=0
b=3


#座標表示の関数
def coordinate(a,b):
    for i in range(0,3):
        print(Board[a:b])
        a=a+3
        b=b+3
    print()

#プレイヤー種類
status=[0,1]

#先攻はユーザー側（初期値）
p_type=status[0]

#勝敗決定フラグ（endは値参照・更新にglobal endが必要）
end=0

#プレイヤー交代の関数
def playertype(p_type):
    global end
    if end==0 and p_type==status[0]:
        p_type=status[1]
        print("現在のターン：CPU")
        
    
    elif end==0 and p_type==status[1]:
        p_type=status[0]
        print("現在のターン：あなた")
    
    

#共通動作×
def func(p_type):
    global end
    if end==0 and p_type==status[0]:#ユーザーターン
        print("座標を入力してください：",end="")
        select=int(input())#座標のキー入力をintで与える
                
        #選択した座標が埋まっているかチェック
        while Board[select] =='o' or Board[select]=='x':
            print('選択できません。座標を選びなおしてください：',end="")
            select=int(input())
            
            
        else:
            Board[select]='o' 
            coordinate(a,b)
            print()
    
    
    elif end==0 and p_type==status[1]:#CPUターン
        select=random.randint(0,8)
        
        #選択した座標が埋まっているかチェック
        while Board[select] =='o' or Board[select]=='x':
            #print("座標を再選択してください")
            select=random.randint(0,8)
            
        
        else:
            Board[select]='x' 
            coordinate(a,b)
            print()

      


#勝利判定
def win():
        global end
        if end==0:
            judge=[[0, 1, 2],[3, 4, 5],[6, 7, 8],[0, 3, 6],[1, 4, 7],[2, 5, 8],[0, 4, 8],[2, 4, 6],]
            for j in range(0,8):
                f=judge[j][0] #1
                s=judge[j][1] #4
                t=judge[j][2] #7
                parts=[f,s,t] #[1,4,7]
            
              
                if Board[f]==Board[s] and Board[s]==Board[t]:
                    print("%dの勝ち"%p_type)
                    end=1
                
        
        #Boardがどこまで埋まったかチェック
        #print("チェック%d"%j)
        #print(Board)
            


#ゲーム進行
print("初期盤面")
coordinate(a,b)
print("ゲーム開始")


while True:
    
    #先攻＝ユーザ
    func(status[0])
    #勝利判定
    win()    
    #攻守交代    
    playertype(status[0])
    
    #後攻＝CPU  
    func(status[1])
    #勝利判定
    win()    
    #攻守交代
    playertype(status[1])