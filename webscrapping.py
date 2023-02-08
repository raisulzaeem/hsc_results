import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import seaborn as sns
import pandas as pd
import numpy as np

chittagong_board = "https://hscresult.bise-ctg.gov.bd/hsc22/22/individual/result_mark_details.php"
comilla_board = "https://hscresult.comillaboard.gov.bd/h22/"

def get_hsc_result(roll_number):
    response = requests.post("https://hscresult.bise-ctg.gov.bd/hsc22/22/individual/result_mark_details.php", data= {"roll":roll_number}) # 104491
    soup = BeautifulSoup(response.content, 'html.parser')
    table_contents = soup.find_all('table',{"class":"tftable2"})[0]
    subjects_marks = table_contents.find_all('td')
    subjects_marks_dict = {subjects_marks[i].text.strip():subjects_marks[i+1].text.strip() for i in range(0,len(subjects_marks),2)}

    return subjects_marks_dict



if __name__=="__main__":

    global_subjects_marks_dict = {}

    for i in tqdm(range(100000, 117705)):
        try:
            result_dict = get_hsc_result(i)
            for subject, result in result_dict.items():
                if subject not in global_subjects_marks_dict:
                    global_subjects_marks_dict[subject] = [result]
                else:
                    global_subjects_marks_dict[subject].append(result)
        except Exception as e:
            print(e.__class__)



    with open("chittagong_subjects_marks_science.json",'w') as f:
        json.dump(global_subjects_marks_dict, f)


    df = pd.DataFrame(dict([ (k,pd.Series([int(s[s.find("(")+1:s.find(")")]) for s in v if s[s.find("(")+1:s.find(")")].isdigit()])) for k,v in global_subjects_marks_dict.items() ]))
    new_df = pd.DataFrame(data=np.c_[df["PHYSICS(174)"],df["CHEMISTRY(176)"],df["HIGHER MATHEMATICS(265)"]], columns=["Physics","Chemistry","Math"])
    born_plot = sns.displot(data=new_df, kde=True, fill=True, palette=sns.color_palette('bright')[:3], height=15, aspect=1.5, bins=[i for i in range(201)])
    born_plot.fig.suptitle("HSC 2022 Chittagong Board mark distribution")
    born_plot.savefig("Chittagong_board.png", dpi=600)