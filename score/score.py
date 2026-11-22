

from string import printable
from itertools import product
import numpy as np

import string as str
import pandas as pd

df = pd.read_csv("ksgr_scores_revised.csv")
choices = ["A", "B", "C"]


score_types = ["Dominance", "Submission", "Reaction", "Sensation", "Sweet", "Cool", "Progression", "Immersion"]
score_columns = [
    col for col in df.columns
    if col not in ["Q", "option"]
]
# 10問の3択をすべて生成
all_answers = product(range(3), repeat=10)

results = []

for answers in all_answers:
    scores = {key: 0 for key in score_types}

    for question_index, answer_index in enumerate(answers):
        # CSVの該当する回答の点数を加算
        row = df.iloc[question_index * 3 + answer_index]

        for key in score_types:
            scores[key] += row[key]

    results.append(scores)

result_df = pd.DataFrame(results)
res_df = pd.DataFrame({
    "cool" :result_df["Cool"]/max(result_df["Cool"]),
    "sweet":result_df["Sweet"]/ max(result_df["Sweet"]),
    "prog" :result_df["Progression"]/max(result_df["Progression"]),
    "imm"  :result_df["Immersion"]/max(result_df["Immersion"]),
    "reac" :result_df["Reaction"]/max(result_df["Reaction"]),
    "sens" :result_df["Sensation"]/max(result_df["Sensation"]),
    "domi" :result_df["Dominance"]/max(result_df["Dominance"]),
    "subm" :result_df["Submission"]/max(result_df["Submission"])
})
resrate_df = pd.DataFrame({
    "cl" : res_df["cool"]/(res_df["cool"]+res_df["sweet"]),
    "swt" : res_df["sweet"] / (res_df["cool"] + res_df["sweet"]),

    "prog": res_df["prog"] / (res_df["prog"] + res_df["imm"]),
    "imm" : res_df["imm"]  / (res_df["prog"] + res_df["imm"]),

    "reac": res_df["reac"] / (res_df["reac"] + res_df["sens"]),
    "sens": res_df["sens"] / (res_df["reac"] + res_df["sens"]),

    "domi": res_df["domi"] / (res_df["domi"] + res_df["subm"]),
    "subm": res_df["subm"] / (res_df["domi"] + res_df["subm"])
})


cor = result_df.corr()
cor1=res_df.corr()
np.var(result_df["Submission"])
np.var(result_df["Dominance"])

max(result_df["Sweet"])
max(result_df["Cool"])
max(result_df["Dominance"])
max(result_df["Submission"])
max(result_df["Immersion"])
max(result_df["Progression"])
max(result_df["Reaction"])
max(result_df["Sensation"])


import matplotlib.pyplot as plt

plt.figure(figsize=(7, 7))
plt.scatter(resrate_df["reac"], resrate_df["sens"])

# 対立軸
axes = [
    ("Sweet", "Cool"),
    ("Dominance", "Submission"),
    ("Reaction", "Sensation"),
    ("Progression", "Immersion")
]
axe = [
    ("S", "C"),
    ("D", "S"),
    ("R", "S"),
    ("P", "I")
]

# 各軸の勝者からタイプを決定
def classify(num,sweet, cool):
    if sweet > cool:
        return axe[num][0]
    elif sweet < cool:
        return axe[num][1]
    else:
        return "X"

TYPE_K = result_df.apply(
     lambda row: classify(0,row[axes[0][0]], row[axes[0][1]]),
     axis=1
)
TYPE_S = result_df.apply(
     lambda row: classify(3,row[axes[3][0]], row[axes[3][1]]),
     axis=1
)
TYPE_G = result_df.apply(
     lambda row: classify(2,row[axes[2][0]], row[axes[2][1]]),
     axis=1
)
TYPE_R = result_df.apply(
    lambda row: classify(1,row[axes[1][0]], row[axes[1][1]]),
    axis=1
)
axes = [
    ("sweet", "cool"),
    ("domi", "subm"),
    ("reac", "sens"),
    ("prog", "imm")
]
k = res_df.apply(
     lambda row: classify(0,row[axes[0][0]], row[axes[0][1]]),
     axis=1
)
s = res_df.apply(
     lambda row: classify(3,row[axes[3][0]], row[axes[3][1]]),
     axis=1
)
g = res_df.apply(
     lambda row: classify(2,row[axes[2][0]], row[axes[2][1]]),
     axis=1
)
r = res_df.apply(
    lambda row: classify(1,row[axes[1][0]], row[axes[1][1]]),
    axis=1
)




TYPE = TYPE_K.str.cat(TYPE_S).str.cat(TYPE_G).str.cat(TYPE_R)
#TYPE_K.value_counts().plot(kind="bar")
TYPE_K.value_counts()
k.value_counts()
TYPE_S.value_counts()
s.value_counts()
TYPE_G.value_counts()
g.value_counts()
TYPE_R.value_counts()
r.value_counts()
type_res = k.str.cat(s).str.cat(g).str.cat(r)
type_res_count =type_res.value_counts()
type_res_count
3**(10)/16
type_counts =TYPE.value_counts()
TYPE_df = pd.DataFrame({
    "K": TYPE_K,
    "S": TYPE_S,
    "G": TYPE_G,
    "R": TYPE_R,
    "type" : TYPE
})
(~TYPE_df.eq("X").any(axis=1)).sum()/len(TYPE_df)

len(TYPE_df)/16
result_df[result_df["Cool"]==result_df["Sweet"]]
type_df = pd.DataFrame({
    "K": k,
    "S": s,
    "G": g,
    "R": r,
    "type" : type
})

g_adjust_table = {
    ("C", "P", "D"): "S",
    ("C", "P", "S"): "S",
    ("C", "I", "D"): "R",
    ("C", "I", "S"): "R",
    ("S", "P", "D"): "S",
    ("S", "P", "S"): "R",
    ("S", "I", "D"): "R",
    ("S", "I", "S"): "R",
}

def adjust_g(row):
    if row["G"] == "X":
        return g_adjust_table.get(
            (row["K"], row["S"], row["R"]),
            "X"
        )
    return row["G"]

g_adj= type_df.apply(adjust_g, axis=1)
g_adj.value_counts()
type_adj = k.str.cat(s).str.cat(g_adj).str.cat(r)
type_adj.value_counts()
