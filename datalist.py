import sqlite3
import pandas as pd


create_table_query="""
CREATE TABLE IF NOT EXISTS stable_diffusion(
    idx INTEGER PRIMARY KEY,
    User	TEXT,
	stdname	TEXT NOT NULL,
    positive_prompt TEXT NOT NULL,
    nagative_prompt TEXT,
    filter TEXT NOT NULL,
    uploaded_file TEXT,
    noise TEXT NOT NULL,
    cfg REAL NOT NULL,
    steps INTEGER NOT NULL,
    result_file TEXT NOT NULL,
    share INTEGER NOT NULL
);
"""
# def create_table_from_csv(csv_file, table_name):
#     # SQLite 데이터베이스 파일 생성 또는 연결
#     conn = sqlite3.connect('stdlist.db')

#     # CSV 파일을 pandas DataFrame으로 읽어오기
#     df = pd.read_csv(csv_file)

#     # DataFrame을 SQLite 테이블로 저장
#     df.to_sql(table_name, conn, if_exists='replace', index=False)

#     # 연결 종료
#     conn.close()

# # 사용 예시
# create_table_from_csv('stdlist.csv', 'stable_diffusion')

def create_table():
    list = sqlite3.connect('stdlist.db')
    cursor = list.cursor()
    
    # 이미 테이블이 생성되었는지 확인
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stable_diffusion';")
    if cursor.fetchone() is None:
        # 테이블이 아직 생성되지 않은 경우 테이블 생성
        cursor.execute(create_table_query)  
        list.commit() 
    list.close()
     
#정보 저장
def save(index, username, stdname, pprompt, nprompt, f, uf, noise, cfg, steps, rf, share):   
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    insert_data_query='''
    INSERT INTO stable_diffusion(idx, User, stdname, positive_prompt, 
    nagative_prompt, filter, uploaded_file, noise, cfg, steps, result_file, share)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
    '''
    
    data_to_insert = (index, username, stdname, pprompt, nprompt, f, uf, noise, cfg, steps, rf, share)
    
    cursor.execute(insert_data_query, data_to_insert)

    list.commit()
    list.close()
    return None

#저장된 데이터 전부 불러오기
def load_list(stdname):
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    data_list=[]
    if(stdname=="all"):
        select_data_query='''
        SELECT * FROM stable_diffusion WHERE share=1;
        '''
        cursor.execute(select_data_query)
    else:
        select_data_query='''
        SELECT * FROM stable_diffusion WHERE stdname=? AND share=1;
        '''
        cursor.execute(select_data_query, (stdname,))
    
    
    data=cursor.fetchall()
    
    for row in data:
        data_list.append(row)
        
    list.commit()
    list.close()
    return data_list

#저장된 데이터 전부 불러오기
def user_load_list(stdname, user):
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    data_list=[]
    if(stdname=="all"):
        select_data_query='''
        SELECT * FROM stable_diffusion WHERE User=?;
        '''
        cursor.execute(select_data_query,(user,))
    else:
        select_data_query='''
        SELECT * FROM stable_diffusion WHERE stdname=? AND share=1 AND User=?;
        '''
        cursor.execute(select_data_query, (stdname, user,))
    
    
    data=cursor.fetchall()
    
    for row in data:
        data_list.append(row)
        
    list.commit()
    list.close()
    return data_list

#특정 인덱스 값 가져오기
def Now_idx():    
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    select_data_query = "SELECT COUNT(*) FROM stable_diffusion;"
    cursor.execute(select_data_query)
    row = cursor.fetchone()
    count=row[0]
    
    list.commit()
    list.close()
    return count+1

#특정 인덱스 값의 데이터 가져오기
def load_std(idx):
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    select_data_query='''
    SELECT * FROM stable_diffusion WHERE idx=?;
    '''
    cursor.execute(select_data_query,(idx,))
    data=cursor.fetchall()
    
    list.commit()
    list.close()
    print(data)
    return data

def delete(idx):
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    delete_data_query="DELETE FROM stable_diffusion WHERE idx=?"
    cursor.execute(delete_data_query,(idx,))
    list.commit()
    list.close()
    return None

# for i in range(49,59):
#     delete(i)