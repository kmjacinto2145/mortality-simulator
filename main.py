# -*- coding: utf-8 -*-
"""
Created on Sun May  2 23:02:57 2021

@author: Mick4
"""

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, render_template

#Data import
aus_male_table = pd.read_csv("AusMaleTables.csv")
aus_female_table = pd.read_csv("AusFemaleTables.csv")

#parameters
SIMULATIONS = 100

def simulate_life(age, table):
    current_age = age
    alive = True
    while alive:
        qx = table[table["Age"] == current_age]["qx"]
        is_dead = np.random.binomial(n = 1, p = qx, size = 1)[0]
        if is_dead == 1:
            alive = False
        current_age += 1
    return current_age

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def landing():
    return render_template("landing.html")


@app.route('/results', methods = ["GET", "POST"])
def results():
    age = int(request.form['age'])
    sex = request.form['sex']

    if sex == "Male":
        table = aus_male_table
    elif sex == "Female":
        table = aus_female_table

    simulated_lives = np.array([])

    for i in range(SIMULATIONS):
        simulated_lives = np.append(simulated_lives, simulate_life(age, table))

    median_age = np.median(simulated_lives)
    confint_80 = sp.stats.t.interval(alpha = 0.8, df = len(simulated_lives) - 1, loc = np.mean(simulated_lives), scale = sp.stats.sem(simulated_lives))
    prob_90 = round(confint_80[0], 2)

    return render_template("results.html", median_age = median_age, prob_90 = prob_90)

if __name__ == "__main__":
    app.run(debug=True)
