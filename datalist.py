import sqlite3
import pandas as pd

list=sqlite3.connect('stdlist.db')

df=pd.read_csv("stdlist.csv")

df.to_sql('stable_diffution', list, if_exists='replace', index=False)

list.close()

#정보 저장
def save(pprompt, nprompt, filter, uploaded_file):
    list=sqlite3.connect('stdlist.db')

    cursor=list.cursor()

    create_table_query="""
    CREATE TABLE IF NOT EXISTS stable_diffution(
        index INTEGER PRIMARY KEY,
        positive prompt TEXT NOT NULL,
        nagative prompt TEXT,
        filter TEXT,
        uploaded_file TEXT
    );
    """

    cursor.execute(create_table_query)

    insert_data_query='''
    INSERT INTO stable_diffution(positive prompt, negative prompt, filter, uploaded_file)
    VALUES(?,?,?,?);
    '''
    
    data_to_insert = [
        (pprompt, nprompt, filter, uploaded_file)
    ]
    
    cursor.executemany(insert_data_query, data_to_insert)

    list.commit()

    list.close()
    return None

#저장된 데이터 전부 불러오기
def load_list():
    data_list=[]
    list=sqlite3.connect('stdlist.db')

    cursor=list.cursor()
    
    select_data_query='''
    SELECT * FROM stable-_diffution;
    '''
    cursor.execute(select_data_query)
    data=cursor.fetchall()
    
    for row in data:
        data_list.append(row)
        
    list.close()
    print(data_list)
    return data_list

#특정 인덱스 값 가져오기
def Now_idx():
    lsit=sqlite3.connect('stdlist.db')
    
    cursor=lsit.cursor()
    
    select_data_query='''
    SELECT COUNT(*) FROM students;
    '''
    
    cursor.execute(select_data_query)
    count=cursor.fetchone()[0]
    
    list.close()
    return count

#특정 인덱스 값의 데이터 가져오기
def load_std(idx):
    return None