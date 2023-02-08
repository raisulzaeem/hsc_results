import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import seaborn as sns
import pandas as pd
import numpy as np

chittagong_board = "https://hscresult.bise-ctg.gov.bd/hsc22/22/individual/result_mark_details.php"
comilla_board = "https://hscresult.comillaboard.gov.bd/h22/"
all_subjects = ['BANGLA(101)', 'ENGLISH(107)', 'INFORMATION & COMMUNICATION TECHNOLOGY(275)', 'PHYSICS(174)', 'CHEMISTRY(176)', 'BIOLOGY(178)', 
                'HIGHER MATHEMATICS(265)', 'STATISTICS(129)', 'AGRICULTURE STUDIES(239)', 'PSYCHOLOGY(123)', 'ECONOMICS(109)', 'CIVICS & GOOD GOVERNCE(269)', 
                'HISTORY(304)', 'LOGIC(121)', 'ENGINEERING DRAWING & WORKSHOP PRACTICE(180)']

def get_hsc_result(roll_number):
    response = requests.post("https://hscresult.bise-ctg.gov.bd/hsc22/22/individual/result_mark_details.php", data= {"roll":roll_number}) # 104491
    soup = BeautifulSoup(response.content, 'html.parser')
    table_contents = soup.find_all('table')
    individual_data = {}
    for table_content in table_contents:
        subjects_marks = table_content.find_all('td')
        individual_data.update({subjects_marks[i].text.strip():subjects_marks[i+1].text.strip() for i in range(0,len(subjects_marks),2)})
    
    for subject in all_subjects: 
        if subject not in individual_data:
            individual_data[subject] = 'NA'
    
    df = pd.DataFrame.from_dict(individual_data, orient='index').T
    return df



if __name__=="__main__":

    global_subjects_marks_dict = {}

    full_df = get_hsc_result(100001)

    for i in tqdm(range(100002, 117705)):
        try:
            result_df = get_hsc_result(i)
            full_df = pd.concat([full_df, result_df])
        except Exception as e:
            print(e.__class__)
    
    full_df.to_excel("dataset_chittagong_hsc_2022.xlsx")


    # TODO: 1. Create a new plot taking colleges into consideration 2. Subjectwise bubles to represent the number of students
    # df = pd.DataFrame(dict([ (k,pd.Series([int(s[s.find("(")+1:s.find(")")]) for s in v if s[s.find("(")+1:s.find(")")].isdigit()])) for k,v in global_subjects_marks_dict.items() ]))
    # new_df = pd.DataFrame(data=np.c_[df["PHYSICS(174)"],df["CHEMISTRY(176)"],df["HIGHER MATHEMATICS(265)"]], columns=["Physics","Chemistry","Math"])
    # born_plot = sns.displot(data=new_df, kde=True, fill=True, palette=sns.color_palette('bright')[:3], height=15, aspect=1.5, bins=[i for i in range(201)])
    # born_plot.fig.suptitle("HSC 2022 Chittagong Board mark distribution")
    # born_plot.savefig("Chittagong_board.png", dpi=600)