import numpy as np
import plotly.utils
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo
import base64
from io import BytesIO
import json
# from wtforms.validators import InputRequired



import re
from os import path

# imports the flask app we configured in the websites folder:
from website import create_app

app = create_app()

symptom = ["Fatigue", "Minimum exercise", "Sleep", "Remember"]
pagenum = 0
end = False
pemdomain = 0
sleepdomain = 0
cogdomain = 0
survey = 'classic'
message = "Please enter a response for both frequency and severity before continuing"
composite = 0
pemname = str
sleepname = str
cogname = str

# used for the full-form results
def diagnose2():
    import domainScores as ds
    pem_domainscore = (int(session["minexf"]) + int(session["minexs"]) + int(session['soref']) + int(session['sores']) +
                       int(session['heavyf']) + int(session['heavys']) + int(session['drainedf']) + int(
                session['draineds']) +
                       int(session['mentalf']) + int(session['mentals']) + int(session['weakf']) + int(
                session['weaks'])) / 12

    sleep_domainscore = (int(session["sleepf"]) + int(session["sleeps"]) + int(session['napf']) + int(session['naps']) +
                         int(session['fallf']) + int(session['falls']) + int(session['stayf']) + int(session['stays']) +
                         int(session['earlyf']) + int(session['earlys']) + int(session['alldayf']) + int(
                session['alldays'])) / 12

    cog_domainscore = (int(session["rememberf"]) + int(session["remembers"]) + int(session['attentionf']) +
                       int(session['attentions']) + int(session['wordf']) + int(session['words']) +
                       int(session['understandf']) + int(session['understands']) + int(session['focusf']) +
                       int(session['focuss']) + int(session['slowf']) + int(session['slows']) +
                       int(session['absentf']) + int(session['absents']) + int(session['visionf']) +
                       int(session['visions'])) / 16
    pain_domainscore = (int(session['musclef']) + int(session['muscles']) + int(session['jointpainf']) +
                        int(session['jointpains']) + int(session['eyepainf']) + int(session['eyepains']) +
                        int(session['headachesf']) + int(session['headachess'])) / 8
    gastro_domainscore = (int(session['bloatf']) + int(session['bloats']) + int(session['bowelf']) +
                          int(session['bowels']) + int(session['stomachf']) + int(session['stomachs']) +
                          int(session['bladderf']) + int(session['bladders'])) / 8
    ortho_domainscore = (int(session['unsteadyf']) + int(session['unsteadys']) + int(session['chestpainf']) +
                         int(session['chestpains']) + int(session['shortf']) + int(session['shorts']) +
                         int(session['dizzyf']) + int(session['dizzys']) + int(session['heartf']) +
                         int(session['hearts']) + int(session['nauseaf']) + int(session['nauseas'])) / 12
    circ_domainscore = (int(session['limbsf']) + int(session['limbss']) + int(session['hotf']) +
                        int(session['hots']) + int(session['lotempf']) + int(session['lotemps']) +
                        int(session['sweatf']) + int(session['sweats']) + int(session['chillsf']) +
                        int(session['chillss']) + int(session['weightf']) + int(session['weights']) +
                        int(session['appetitef']) + int(session['appetites']) + int(session['nightf']) +
                        int(session['nights'])) / 16
    immune_domainscore = (int(session['fluf']) + int(session['flus']) + int(session['feverf']) +
                          int(session['fevers']) + int(session['lymphnodesf']) + int(session['lymphnodess']) +
                          int(session['throatf']) + int(session['throats']) + int(session['hitempf']) +
                          int(session['hitemps'])) / 10
    neuroen_domainscore = (int(session['smellf']) + int(session['smells']) + int(session['alcoholf']) +
                           int(session['alcohols']) + int(session['twitchesf']) + int(session['twitchess']) +
                           int(session['noisef']) + int(session['noises']) + int(session['lightsf']) +
                           int(session['lightss']) + int(session['depthf']) + int(session['depths'])) / 12

    mecfs = ds.df[(ds.df['dx'] == 1)]
    control = ds.df[(ds.df['dx'] != 1)]
    user_scores = [(int(session['fatiguescoref']) + int(session['fatiguescores'])) / 2,
                   pem_domainscore, sleep_domainscore, cog_domainscore, pain_domainscore, gastro_domainscore,
                   ortho_domainscore, circ_domainscore, immune_domainscore, neuroen_domainscore]
    cfsDomains = np.mean(mecfs.iloc[:, 110:120], axis=0)
    conDomains = np.mean(control.iloc[:, 110:120], axis=0)

    categories = ['Fatigue', 'PEM', 'Sleep', 'Cognitive Problems', 'Pain', 'Gastro Problems',
                  'Orthostatic Intolerance', 'Circulatory Problems', 'Immune System', 'Neuroendocrine Problems']

    # IOM assessment
    iomfatiguecheck = "No"
    iomreductioncheck = "No"
    iompemcheck = "No"
    iomsleepcheck = "No"
    iomcogcheck = "No"
    if int(session['fatiguescoref']) >= 2 and int(session['fatiguescores']) >= 2:
        iomfatiguecheck = "Yes"
    if int(session['reduction']) == 1:
        iomreductioncheck = "Yes"
    if (int(session['minexf']) >= 2 and int(session['minexs']) >= 2) or (
            int(session['heavyf']) >= 2 and int(session['heavys']) >= 2) or \
            (int(session['soref']) >= 2 and int(session['sores']) >= 2) or (
            int(session['mentalf']) >= 2 and int(session['mentals']) >= 2) or \
            (int(session['drainedf']) >= 2 and int(session['draineds']) >= 2):
        iompemcheck = "Yes"
    if (int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2) or (
            int(session['napf']) >= 2 and int(session['naps']) >= 2) or \
            (int(session['fallf']) >= 2 and int(session['falls']) >= 2) or (
            int(session['stayf']) >= 2 and int(session['stays']) >= 2) or \
            (int(session['earlyf']) >= 2 and int(session['earlys']) >= 2) or (
            int(session['alldayf']) >= 2 and int(session['alldays']) >= 2):
        iomsleepcheck = "Yes"
    if (int(session['lightsf']) >= 2 and int(session['lightss']) >= 2) or \
        (int(session['rememberf']) >= 2 and int(session['remembers']) >= 2) or \
        (int(session['attentionf']) >= 2 and int(session['attentions']) >= 2) or \
        (int(session['wordf']) >= 2 and int(session['words']) >= 2) or (
        int(session['understandf']) >= 2 and int(session['understands']) >= 2) or \
        (int(session['focusf']) >= 2 and int(session['focuss']) >= 2) or (
        int(session['visionf']) >= 2 and int(session['visions']) >= 2) or \
        (int(session['depthf']) >= 2 and int(session['depths']) >= 2) or (
        int(session['slowf']) >= 2 and int(session['slows']) >= 2) or \
        (int(session['absentf']) >= 2 and int(session['absents']) >= 2):
        iomcogcheck = "Yes"

    if iomfatiguecheck == "Yes" and iomreductioncheck == "Yes" and iompemcheck == "Yes" and iomsleepcheck == "Yes" and iomcogcheck == "Yes":
        iom_msg = "Your responses suggest you meet the IOM Criteria for ME/CFS."
        iomdxcheck = "Met"

    else:
        iom_msg = "Your responses do not meet the IOM Criteria for ME/CFS."
        iomdxcheck = "Not met"

    # Canadian criteria assessment
    ccc_dx = False

    if int(session['fatiguescoref']) >= 2 and int(session['fatiguescores']) >= 2:
        ccc_fatigue = 1

        ccc_fatiguecheck = "Yes"
    else:
        ccc_fatigue = 0
        ccc_fatiguecheck = "No"
    if int(session['reduction']) == 1:
        ccc_reduction = "Yes"
    else:
        ccc_reduction = "No"
    if (int(session['musclef']) >= 2 and int(session['muscles']) >= 2) or (
            int(session['jointpainf']) >= 2 and int(session['jointpains']) >= 2) or \
            (int(session['eyepainf']) >= 2 and int(session['eyepains']) >= 2) or (
            int(session['chestpainf']) >= 2 and int(session['chestpains']) >= 2) or \
            (int(session['headachesf']) >= 2 and int(session['headachess']) >= 2) or (
            int(session['bloatf']) >= 2 and int(session['bloats']) >= 2) or \
            (int(session['stomachf']) >= 2 and int(session['stomachs']) >= 2):
        ccc_pain = 1
        ccc_paincheck = "Yes"
    else:
        ccc_pain = 0
        ccc_paincheck = "No"
    if int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2:
        ccc_sleep = 1
        ccc_sleepcheck = "Yes"
    else:
        ccc_sleep = 0
        ccc_sleepcheck = "No"
    if (int(session['minexf']) >= 2 and int(session['minexs']) >= 2) or (
            int(session['soref']) >= 2 and int(session['sores']) >= 2):
        ccc_pem = 1
        ccc_pemcheck = "Yes"
    else:
        ccc_pem = 0
        ccc_pemcheck = "No"
    if (int(session['twitchesf']) >= 2 and int(session['twitchess']) >= 2) or (
            int(session['weakf']) >= 2 and int(session['weaks']) >= 2) or \
            (int(session['noisef']) >= 2 and int(session['noises']) >= 2) or (
            int(session['lightsf']) >= 2 and int(session['lightss']) >= 2) or \
            (int(session['rememberf']) >= 2 and int(session['remembers']) >= 2) or \
            (int(session['attentionf']) >= 2 and int(session['attentions']) >= 2) or \
            (int(session['wordf']) >= 2 and int(session['words']) >= 2) or (
            int(session['understandf']) >= 2 and int(session['understands']) >= 2) or \
            (int(session['focusf']) >= 2 and int(session['focuss']) >= 2) or (
            int(session['visionf']) >= 2 and int(session['visions']) >= 2) or \
            (int(session['depthf']) >= 2 and int(session['depths']) >= 2) or (
            int(session['slowf']) >= 2 and int(session['slows']) >= 2) or \
            (int(session['absentf']) >= 2 and int(session['absents']) >= 2):
        ccc_cog = 1
        ccc_cogcheck = "Yes"
    else:
        ccc_cog = 0
        ccc_cogcheck = "No"

    if (int(session['unsteadyf']) >= 2 and int(session['unsteadys']) >= 2) or (
            int(session['bowelf']) >= 2 and int(session['bowels']) >= 2) or \
            (int(session['bladderf']) >= 2 and int(session['bladders']) >= 2) or (
            int(session['nauseaf']) >= 2 and int(session['nauseas']) >= 2) or (
            int(session['shortf']) >= 2 and int(session['shorts']) >= 2) or (
            int(session['dizzyf']) >= 2 and int(session['dizzys']) >= 2) or (
            int(session['heartf']) >= 2 and int(session['hearts']) >= 2):
        ccc_auto = 1
        ccc_autocheck = "Yes"
    else:
        ccc_auto = 0
        ccc_autocheck = "No"
    if (int(session['sweatf']) >= 2 and int(session['sweats']) >= 2) or (
            int(session['nightf']) >= 2 and int(session['nights']) >= 2) or \
            (int(session['limbsf']) >= 2 and int(session['limbss']) >= 2) or (
            int(session['chillsf']) >= 2 and int(session['chillss']) >= 2) or \
            (int(session['hotf']) >= 2 and int(session['hots']) >= 2) or (
            int(session['hitempf']) >= 2 and int(session['hitemps']) >= 2) or \
            (int(session['lotempf']) >= 2 and int(session['lotemps']) >= 2) or (
            int(session['appetitef']) >= 2 and int(session['appetites']) >= 2) or (
            int(session['weightf']) >= 2 and int(session['weights']) >= 2) or (
            int(session['alcoholf']) >= 2 and int(session['alcohols']) >= 2):
        ccc_neuro = 1
        ccc_neurocheck = "Yes"
    else:
        ccc_neuro = 0
        ccc_neurocheck = "No"
    if (int(session['fluf']) >= 2 and int(session['flus']) >= 2) or (
            int(session['smellf']) >= 2 and int(session['smells']) >= 2) or \
            (int(session['throatf']) >= 2 and int(session['throats']) >= 2) or \
            (int(session['lymphnodesf']) >= 2 and int(session['lymphnodess']) >= 2) or \
            (int(session['feverf']) >= 2 and int(session['fevers']) >= 2):
        ccc_immune = 1
        ccc_immunecheck = "Yes"
    else:
        ccc_immune = 0
        ccc_immunecheck = "No"
    ccc_poly = np.sum([ccc_auto, ccc_neuro, ccc_immune])
    # most of the symptoms are required, but there is one polythetic criteria, shown here by ccc_poly
    if np.sum([ccc_fatigue, ccc_pem, ccc_sleep, ccc_pain, ccc_cog]) >= 5 and ccc_poly >= 2:
        ccc_dx = "Met"
        ccc_msg = "Your responses suggest that you meet the Canadian Consensus Criteria for ME/CFS."
    else:
        ccc_dx = "Not met"
        ccc_msg = "Your responses do not meet the Canadian Consensus Criteria for ME/CFS."

    # ME-ICC assessment starts here, the longest and most complicated assessment
    if int(session['reduction']) == 1:
        ME_R = 1
    else:
        ME_R = 0

    if (int(session['minexf']) >= 2 and int(session['minexs']) >= 2) or (
            int(session['heavyf']) >= 2 and int(session['heavys']) >= 2) or \
            (int(session['soref']) >= 2 and int(session['sores']) >= 2) or (
            int(session['mentalf']) >= 2 and int(session['mentals']) >= 2) or \
            (int(session['drainedf']) >= 2 and int(session['draineds']) >= 2):
        ME_A = 1
        meicc_pemcheck = "Yes"
    else:
        ME_A = 0
        meicc_pemcheck = "No"
    print(ME_A)
    if (int(session['rememberf']) >= 2 and int(session['remembers']) >= 2) or (
            int(session['attentionf']) >= 2 and int(session['attentions']) >= 2) or \
            (int(session['wordf']) >= 2 and int(session['words']) >= 2) or (
            int(session['understandf']) >= 2 and int(session['understands']) >= 2) or \
            (int(session['focusf']) >= 2 and int(session['focuss']) >= 2) or (
            int(session['visionf']) >= 2 and int(session['visions']) >= 2) or \
            (int(session['depthf']) >= 2 and int(session['depths']) >= 2) or (
            int(session['slowf']) >= 2 and int(session['slows']) >= 2) or \
            (int(session['absentf']) >= 2 and int(session['absents']) >= 2):
        ME_B1 = 1
        meicc_cogcheck = "Yes"
    else:
        ME_B1 = 0
        meicc_cogcheck = "No"
    print(ME_B1)
    if (int(session['musclef']) >= 2 and int(session['muscles']) >= 2) or (
            int(session['jointpainf']) >= 2 and int(session['jointpains']) >= 2) or \
            (int(session['eyepainf']) >= 2 and int(session['eyepains']) >= 2) or (
            int(session['chestpainf']) >= 2 and int(session['chestpains']) >= 2) or \
            (int(session['headachesf']) >= 2 and int(session['headachess']) >= 2):
        ME_B2 = 1
        meicc_paincheck = "Yes"
    else:
        ME_B2 = 0
        meicc_paincheck = "No"
    print(ME_B2)
    if (int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2) or (
            int(session['napf']) >= 2 and int(session['naps']) >= 2) or \
            (int(session['fallf']) >= 2 and int(session['falls']) >= 2) or (
            int(session['stayf']) >= 2 and int(session['stays']) >= 2) or \
            (int(session['earlyf']) >= 2 and int(session['earlys']) >= 2) or (
            int(session['alldayf']) >= 2 and int(session['alldays']) >= 2):
        ME_B3 = 1
        meicc_sleepcheck = "Yes"
    else:
        ME_B3 = 0
        meicc_sleepcheck = "No"
    print(ME_B3)
    if (int(session['twitchesf']) >= 2 and int(session['twitchess']) >= 2) or (
            int(session['weakf']) >= 2 and int(session['weaks']) >= 2) or \
            (int(session['noisef']) >= 2 and int(session['noises']) >= 2) or (
            int(session['lightsf']) >= 2 and int(session['lightss']) >= 2) or \
            (int(session['unsteadyf']) >= 2 and int(session['unsteadys']) >= 2):
        ME_B4 = 1
        meicc_motorcheck = "Yes"
    else:
        ME_B4 = 0
        meicc_motorcheck = "No"
    print(ME_B4)
    if (ME_B1 + ME_B2 + ME_B3 + ME_B4) >= 3:
        ME_B = 1
    else:
        ME_B = 0
    print(ME_B)
    if (int(session['throatf']) >= 2 and int(session['throats']) >= 2) or (
            int(session['lymphnodesf']) >= 2 and int(session['lymphnodess']) >= 2) or \
            (int(session['feverf']) >= 2 and int(session['fevers']) >= 2) or (
            int(session['fluf']) >= 2 and int(session['flus']) >= 2):
        ME_C1 = 1
        meicc_flucheck = "Yes"
    else:
        ME_C1 = 0
        meicc_flucheck = "No"
    print(ME_C1)

    if int(session['viral']) == 1:
        ME_C2 = 1
        meicc_viralcheck = "Yes"
    else:
        ME_C2 = 0
        meicc_viralcheck = "No"
    if (int(session['bloatf']) >= 2 and int(session['bloats']) >= 2) or (
            int(session['stomachf']) >= 2 and int(session['stomachs']) >= 2) or \
            (int(session['bowelf']) >= 2 and int(session['bowels']) >= 2) or (
            int(session['nauseaf']) >= 2 and int(session['nauseas']) >= 2):
        ME_C3 = 1
        meicc_gastrocheck = "Yes"
    else:
        ME_C3 = 0
        meicc_gastrocheck = "No"
    print(ME_C3)
    if int(session['bladderf']) >= 2 and int(session['bladders']) >= 2:
        ME_C4 = 1
        meicc_bladdercheck = "Yes"
    else:
        ME_C4 = 0
        meicc_bladdercheck = "No"
    print(ME_C4)
    if (int(session['alcoholf']) >= 2 and int(session['alcohols']) >= 2) or (
            int(session['smellf']) >= 2 and int(session['smells']) >= 2):
        ME_C5 = 1
        meicc_sensitivitycheck = "Yes"
    else:
        ME_C5 = 0
        meicc_sensitivitycheck = "No"
    print(ME_C5)
    if (ME_C1 + ME_C2 + ME_C3 + ME_C4 + ME_C5) >= 3:
        ME_C = 1
    else:
        ME_C = 0
    print(ME_C)
    if (int(session['dizzyf']) >= 2 and int(session['dizzys']) >= 2) or (
            int(session['heartf']) >= 2 and int(session['hearts']) >= 2):
        ME_D1 = 1
        meicc_cardiocheck = "Yes"
    else:
        ME_D1 = 0
        meicc_cardiocheck = "No"
    print(ME_D1)
    if int(session['shortf']) >= 2 and int(session['shorts']) >= 2:
        ME_D2 = 1
        meicc_respiratorycheck = "Yes"
    else:
        ME_D2 = 0
        meicc_respiratorycheck = "No"
    print(ME_D2)
    if (int(session['sweatf']) >= 2 and int(session['sweats']) >= 2) or (
            int(session['nightf']) >= 2 and int(session['nights']) >= 2) or \
            (int(session['limbsf']) >= 2 and int(session['limbss']) >= 2) or (
            int(session['chillsf']) >= 2 and int(session['chillss']) >= 2) or \
            (int(session['hotf']) >= 2 and int(session['hots']) >= 2) or (
            int(session['hitempf']) >= 2 and int(session['hitemps']) >= 2) or \
            (int(session['lotempf']) >= 2 and int(session['lotemps']) >= 2) or (
            int(session['slowf']) >= 2 and int(session['slows']) >= 2) or \
            (int(session['absentf']) >= 2 and int(session['absents']) >= 2):
        ME_D3 = 1
        meicc_thermocheck = "Yes"
        meicc_tempcheck = "Yes"
    else:
        ME_D3 = 0
        meicc_thermocheck = "No"
        meicc_tempcheck = "No"
    print(ME_D3)
    if (ME_D1 + ME_D2 + ME_D3) >= 1:
        ME_D = 1
    else:
        ME_D = 0
    print(ME_D)
    ME_score = (ME_R + ME_A + ME_B + ME_C + ME_D)
    print(ME_score)
    if ME_score == 5:
        ME_diagnosis = 1
        me_icc = "Your scores suggest you meet the ME-ICC case definition criteria for ME/CFS"
        meicc_dxcheck = "Met"
    else:
        ME_diagnosis = 0
        me_icc = "Your scores suggest you do not meet the ME-ICC case definition criteria for ME/CFS"
        meicc_dxcheck = "Not met"
    fig = go.Figure(
        data=[
            go.Bar(y=cfsDomains, x=categories,
                   name="Average ME/CFS scores"),
            go.Bar(y=user_scores, x=categories, name="Your scores")],
        layout=go.Layout(
            title=go.layout.Title(text='Your scores compared'
                                       ' with our dataset of 2,402 participants'),
            showlegend=True, legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1)))
    fig.update_layout(yaxis_title='Averaged Frequency and Severity Scores',
                      xaxis_title='Symptom Domains')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph3.html", graphJSON=graphJSON,
                           ccc_msg=ccc_msg, ccc_fatiguecheck=ccc_fatiguecheck,
                           ccc_pemcheck=ccc_pemcheck, ccc_paincheck=ccc_paincheck, ccc_sleepcheck=ccc_sleepcheck,
                           ccc_cogcheck=ccc_cogcheck, ccc_autocheck=ccc_autocheck, ccc_immunecheck=ccc_immunecheck,
                           ccc_neurocheck=ccc_neurocheck, ccc_dx=ccc_dx, ccc_reduction=ccc_reduction,
                           iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                           iompemcheck=iompemcheck, iomdxcheck=iomdxcheck, iom_msg=iom_msg,
                           iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck)


@app.route('/graph')
def graph(graphJSON, probCFS, sample_size):
    graphJSON = graphJSON
    probCFS = probCFS
    sample_size = sample_size
    return render_template("graph.html", graphJSON=graphJSON, probCFS=probCFS, sample_size=sample_size)


@app.route('/end2', methods=['get'])
def end2():
    global pagenum
    fatiguescoref = int(session["fatiguescoref"])
    fatiguescores = int(session["fatiguescores"])
    minexf = int(session["minexf"])
    minexs = int(session["minexs"])
    global pemdomain
    global cogdomain
    global sleepdomain

    sleepf = int(session["sleepf"])
    sleeps = int(session["sleeps"])
    rememberf = int(session["rememberf"])
    remembers = int(session["remembers"])

    if pemdomain == 1 and sleepdomain == 1 and cogdomain == 1:
        return f"<h1>{pemdomain}You may have ME/CFS. We advise you to consult a specialist. </h1>"
    else:
        return f"<h1>{pemdomain}You probably don't have ME/CFS</h1>"


@app.route('/soreness', methods=['post', 'get'])
def expem1():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        soref = request.form.get("soref")
        sores = request.form.get("sores")
        if soref is not None and sores is not None:
            session["soref"] = soref
            session["sores"] = sores
            session['pagenum'] += 1

            if int(session["soref"]) >= 0 and int(session["sores"]) >= 0:
                session['pemscoref'] = session['soref']
                session['pemscores'] = session['sores']
                session['pemscore'] = (int(session['soref']) + int(session['sores'])) / 2
                pemname = 'soreness15'

                return redirect(url_for("excog1"))


        else:
            return render_template("expem1.html", pagenum=session['pagenum'], message=message)
    return render_template("expem1.html", pagenum=session['pagenum'], message='')


@app.route('/drained', methods=['post', 'get'])
def expem2():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        drainedf = request.form.get("drainedf")
        draineds = request.form.get("draineds")
        if drainedf is not None and draineds is not None:
            session["drainedf"] = drainedf
            session["draineds"] = draineds
            session['pagenum'] += 1
            if int(session["drainedf"]) >= 0 and int(session["draineds"]) >= 0:
                session['pemscoref'] = session['drainedf']
                session['pemscores'] = session['draineds']
                session['pemscore'] = (int(session['drainedf']) + int(session['draineds'])) / 2
                pemname = 'drained18'
                return redirect(url_for("weakness"))
        else:
            return render_template("expem2.html", pagenum=session['pagenum'], message=message)
    return render_template("expem2.html", pagenum=session['pagenum'], message='')


@app.route('/viral', methods=['post', 'get'])
def viral():
    form = FlaskForm()
    msg_viral = "Please select one of the options before continuing"
    if request.method == 'POST':
        viral = request.form.get('viral')
        if viral is not None:
            session['viral'] = viral
            session['pagenum'] += 1
            return redirect(url_for('expem3'))
        else:
            return render_template("viral.html", message=msg_viral, pagenum=session['pagenum'])
    return render_template('viral.html', message='', pagenum=session['pagenum'])


@app.route('/heavy', methods=['post', 'get'])
def expem3():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        heavyf = request.form.get("heavyf")
        heavys = request.form.get("heavys")

        if heavyf is not None and heavys is not None:
            session["heavyf"] = heavyf
            session["heavys"] = heavys
            session['pagenum'] += 1
            if int(session["heavyf"]) >= 0 and int(session["heavys"]) >= 0:
                session['pemscoref'] = session['heavyf']
                session['pemscores'] = session['heavys']
                session['pemscore'] = (int(session['heavyf']) + int(session['heavys'])) / 2
                pemname = 'heavy14'
                return redirect(url_for("expem4"))
        else:
            return render_template("expem3.html", pagenum=session['pagenum'], message=message)
    return render_template("expem3.html", pagenum=session['pagenum'], message='')


@app.route('/mentally', methods=['post', 'get'])
def expem4():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        mentalf = request.form.get("mentalf")
        mentals = request.form.get("mentals")
        if mentalf is not None and mentals is not None:
            session["mentalf"] = mentalf
            session["mentals"] = mentals
            session['pagenum'] += 1
            if int(session["mentalf"]) >= 0 and int(session["mentals"]) >= 0:
                session['pemscoref'] = int(mentalf)
                session['pemscores'] = int(mentals)
                session['pemscore'] = (int(session['mentalf']) + int(session['mentals'])) / 2
                pemname = 'mental16'
                return redirect(url_for("expem2"))
        else:
            return render_template("expem4.html", message=message, pagenum=session['pagenum'])
    return render_template("expem4.html", message='', pagenum=session['pagenum'])


@app.route('/weakness', methods=['post', 'get'])
def weakness():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        weakf = request.form.get("weakf")
        weaks = request.form.get("weaks")
        if weakf is not None and weaks is not None:
            session["weakf"] = weakf
            session["weaks"] = weaks
            session['pagenum'] += 1
            session['pemscoref'] = int(weakf)
            session['pemscores'] = int(weaks)
            pemname = 'weakness33'
            session['pemscore'] = (int(session['weakf']) + int(session['weaks'])) / 2
            return redirect(url_for("exsleep2"))
        else:
            return render_template("weakness33.html", message=message, pagenum=session['pagenum'])
    return render_template("weakness33.html", message='', pagenum=session['pagenum'])


@app.route('/staying', methods=['post', 'get'])
def exsleep1():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        stayf = request.form.get("stayf")
        stays = request.form.get("stays")
        if stayf is not None and stays is not None:
            session["stayf"] = stayf
            session["stays"] = stays
            session['pagenum'] += 1
            if int(session["stayf"]) >= 0 and int(session["stays"]) >= 0:
                session['sleepscoref'] = int(stayf)
                session['sleepscores'] = int(stays)
                session['sleepscore'] = (int(session['stayf']) + int(session['stays'])) / 2
                sleepname = 'staying22'
                return redirect(url_for("early"))
        else:
            return render_template("exsleep1.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep1.html", message='', pagenum=session['pagenum'])


@app.route('/nap', methods=['post', 'get'])
def exsleep2():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        napf = request.form.get("napf")
        naps = request.form.get("naps")
        if napf is not None and naps is not None:
            session["napf"] = napf
            session["naps"] = naps
            session['pagenum'] += 1

            session['sleepscoref'] = int(napf)
            session['sleepscores'] = int(naps)
            session['sleepscore'] = (int(session['napf']) + int(session['naps'])) / 2
            sleepname = 'nap20'
            return redirect(url_for("exsleep3"))
        else:
            return render_template("exsleep2.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep2.html", message='', pagenum=session['pagenum'])


@app.route('/falling', methods=['post', 'get'])
def exsleep3():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        fallf = request.form.get("fallf")
        falls = request.form.get("falls")
        if fallf is not None and falls is not None:
            session["fallf"] = fallf
            session["falls"] = falls
            session['pagenum'] += 1
            if int(session["fallf"]) >= 0 and int(session["falls"]) >= 0:
                session['sleepscoref'] = int(fallf)
                session['sleepscores'] = int(falls)
                session['sleepscore'] = (int(session['fallf']) + int(session['falls'])) / 2
                sleepname = 'falling21'
                return redirect(url_for("exsleep1"))
        else:
            return render_template("exsleep3.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep3.html", message='', pagenum=session['pagenum'])


@app.route('/early', methods=['post', 'get'])
def early():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        earlyf = request.form.get("earlyf")
        earlys = request.form.get("earlys")
        if earlyf is not None and earlys is not None:
            session["earlyf"] = earlyf
            session["earlys"] = earlys
            session['pagenum'] += 1
            if int(session["earlyf"]) >= 0 and int(session["earlys"]) >= 0:
                session['sleepscoref'] = int(earlyf)
                session['sleepscores'] = int(earlys)
                session['sleepscore'] = (int(session['earlyf']) + int(session['earlys'])) / 2
                sleepname = 'falling21'
                return redirect(url_for("exsleep4"))
        else:
            return render_template("early23.html", message=message, pagenum=session['pagenum'])
    return render_template("early23.html", message='', pagenum=session['pagenum'])


@app.route('/allday', methods=['post', 'get'])
def exsleep4():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        alldayf = request.form.get("alldayf")
        alldays = request.form.get("alldays")
        if alldayf is not None and alldays is not None:
            session["alldayf"] = alldayf
            session["alldays"] = alldays
            session['pagenum'] += 1
            if int(session["alldayf"]) >= 0 and int(session["alldays"]) >= 0:
                session['sleepscoref'] = int(alldayf)
                session['sleepscores'] = int(alldays)
                session['sleepscore'] = (int(session['alldayf']) + int(session['alldays'])) / 2
                sleepname = 'allday24'
                return redirect(url_for("jointpain"))
            else:
                sleepname = 'allday24'
                session['sleepscoref'] = int(alldayf)
                session['sleepscores'] = int(alldays)
                session['sleepscore'] = (int(session['jointpain']) + int(session['alldays'])) / 2
                return redirect(url_for("jointpain"))
        else:
            return render_template("exsleep4.html", message=message, pagenum=session['pagenum'])
    return render_template("exsleep4.html", message='', pagenum=session['pagenum'])


@app.route('/jointpain', methods=['post', 'get'])
def jointpain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        jointpainf = request.form.get("jointpainf")
        jointpains = request.form.get("jointpains")
        if jointpainf is not None and jointpains is not None:
            session["jointpainf"] = jointpainf
            session["jointpains"] = jointpains
            session['pagenum'] += 1
            return redirect(url_for("eyepain"))
        else:
            return render_template("jointpain26.html", message=message, pagenum=session['pagenum'])
    return render_template("jointpain26.html", message='', pagenum=session['pagenum'])


@app.route('/eyepain', methods=['post', 'get'])
def eyepain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        eyepainf = request.form.get("eyepainf")
        eyepains = request.form.get("eyepains")
        if eyepainf is not None and eyepains is not None:
            session["eyepainf"] = eyepainf
            session["eyepains"] = eyepains
            session['pagenum'] += 1
            return redirect(url_for("chestpain"))
        else:
            return render_template("eyepain27.html", message=message, pagenum=session['pagenum'])
    return render_template("eyepain27.html", message='', pagenum=session['pagenum'])


@app.route('/chestpain', methods=['post', 'get'])
def chestpain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        chestpainf = request.form.get("chestpainf")
        chestpains = request.form.get("chestpains")
        if chestpainf is not None and chestpains is not None:
            session["chestpainf"] = chestpainf
            session["chestpains"] = chestpains
            session['pagenum'] += 1
            return redirect(url_for("stomach"))
        else:
            return render_template("chestpain28.html", message=message, pagenum=session['pagenum'])
    return render_template("chestpain28.html", message='', pagenum=session['pagenum'])


@app.route('/stomach', methods=['post', 'get'])
def stomach():
    global end
    form = FlaskForm()
    if request.method == "POST":
        stomachf = request.form.get("stomachf")
        stomachs = request.form.get("stomachs")
        if stomachf is not None and stomachs is not None:
            session["stomachf"] = stomachf
            session["stomachs"] = stomachs
            session['pagenum'] += 1
            return redirect(url_for("headaches"))
        else:
            return render_template("stomach30.html", message=message, pagenum=session['pagenum'])
    return render_template("stomach30.html", message='', pagenum=session['pagenum'])


@app.route('/headaches', methods=['post', 'get'])
def headaches():
    global end
    form = FlaskForm()
    if request.method == "POST":
        headachesf = request.form.get("headachesf")
        headachess = request.form.get("headachess")
        if headachesf is not None and headachess is not None:
            session["headachesf"] = headachesf
            session["headachess"] = headachess
            session['pagenum'] += 1
            return redirect(url_for("twitches"))
        else:
            return render_template("headaches31.html", message=message, pagenum=session['pagenum'])
    return render_template("headaches31.html", message='', pagenum=session['pagenum'])


@app.route('/twitches', methods=['post', 'get'])
def twitches():
    global end
    form = FlaskForm()
    if request.method == "POST":
        twitchesf = request.form.get("twitchesf")
        twitchess = request.form.get("twitchess")
        if twitchesf is not None and twitchess is not None:
            session["twitchesf"] = twitchesf
            session["twitchess"] = twitchess
            session['pagenum'] += 1
            return redirect(url_for("noise"))
        else:
            return render_template("twitches32.html", message=message, pagenum=session['pagenum'])
    return render_template("twitches32.html", message='', pagenum=session['pagenum'])


@app.route('/noise', methods=['post', 'get'])
def noise():
    global end
    form = FlaskForm()
    if request.method == "POST":
        noisef = request.form.get("noisef")
        noises = request.form.get("noises")
        if noisef is not None and noises is not None:
            session["noisef"] = noisef
            session["noises"] = noises
            session['pagenum'] += 1
            return redirect(url_for("lights"))
        else:
            return render_template("noise34.html", message=message, pagenum=session['pagenum'])
    return render_template("noise34.html", message='', pagenum=session['pagenum'])


@app.route('/lights', methods=['post', 'get'])
def lights():
    global end
    form = FlaskForm()
    if request.method == "POST":
        lightsf = request.form.get("lightsf")
        lightss = request.form.get("lightss")
        if lightsf is not None and lightss is not None:
            session["lightsf"] = lightsf
            session["lightss"] = lightss
            session['pagenum'] += 1
            return redirect(url_for("excog2"))
        else:
            return render_template("lights35.html", message=message, pagenum=session['pagenum'])
    return render_template("lights35.html", message='', pagenum=session['pagenum'])


@app.route('/attention', methods=['post', 'get'])
def excog1():
    form = FlaskForm()
    global cogname
    if request.method == "POST":
        attentionf = request.form.get("attentionf")
        attentions = request.form.get("attentions")
        if attentions is not None and attentionf is not None:
            session["attentionf"] = attentionf
            session["attentions"] = attentions
            session['pagenum'] += 1
            if int(session["attentionf"]) >= 0 and int(session["attentions"]) >= 0:
                session['cogscoref'] = int(attentionf)
                session['cogscores'] = int(attentions)
                cogname = 'difficulty37'
                session['cogscore'] = (int(session['attentionf']) + int(session['attentions'])) / 2
                end = True
                return redirect(url_for("musclepain"))
        else:
            return render_template("excog1.html", message=message, pagenum=session['pagenum'])
    return render_template("excog1.html", message='', pagenum=session['pagenum'])


@app.route('/word', methods=['post', 'get'])
def excog2():
    form = FlaskForm()
    global cogname
    global end
    if request.method == "POST":
        wordf = request.form.get("wordf")
        words = request.form.get("words")
        if words is not None and wordf is not None:
            session["wordf"] = wordf
            session["words"] = words
            session['pagenum'] += 1
            if int(session["wordf"]) >= 0 and int(session["words"]) >= 0:
                session['cogscoref'] = int(wordf)
                session['cogscores'] = int(words)
                session['cogscore'] = (int(session['wordf']) + int(session['words'])) / 2
                return redirect(url_for("understand"))
        else:
            return render_template("excog2.html", message=message, pagenum=session['pagenum'])
    return render_template("excog2.html", message='', pagenum=session['pagenum'])


@app.route('/focus', methods=['post', 'get'])
def excog3():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        focusf = request.form.get("focusf")
        focuss = request.form.get("focuss")
        if focuss is not None and focusf is not None:
            session["focusf"] = focusf
            session["focuss"] = focuss
            session['pagenum'] += 1
            if int(session["focusf"]) >= 0 and int(session["focuss"]) >= 0:
                session['cogscoref'] = int(focusf)
                session['cogscores'] = int(focuss)
                session['cogscore'] = (int(session['focusf']) + int(session['focuss'])) / 2
                # end = True
                cogname = 'focus40'
                return redirect(url_for('vision'))
        else:
            return render_template("excog3.html", message=message, pagenum=session['pagenum'])
    return render_template("excog3.html", message='', pagenum=session['pagenum'])


@app.route('/understand', methods=['post', 'get'])
def understand():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        understandf = request.form.get("understandf")
        understands = request.form.get("understands")
        if understandf is not None and understands is not None:
            session["understandf"] = understandf
            session["understands"] = understands
            session['pagenum'] += 1
            if int(session["understandf"]) >= 0 and int(session["understands"]) >= 0:
                session['cogscoref'] = int(understandf)
                session['cogscores'] = int(understands)
                session['cogscore'] = (int(session['understandf']) + int(session['understands'])) / 2
                # end = True
                cogname = 'understand39'
                return redirect(url_for("excog3"))
        else:
            return render_template("understand39.html", message=message, pagenum=session['pagenum'])
    return render_template("understand39.html", message='', pagenum=session['pagenum'])


@app.route('/slowness', methods=['post', 'get'])
def slowness():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        slowf = request.form.get("slowf")
        slows = request.form.get("slows")
        if slowf is not None and slows is not None:
            session["slowf"] = slowf
            session["slows"] = slows
            session['pagenum'] += 1
            if int(session["slowf"]) >= 0 and int(session["slows"]) >= 0:
                session['cogscoref'] = int(slowf)
                session['cogscores'] = int(slows)
                session['cogscore'] = (int(session['slowf']) + int(session['slowf'])) / 2
                # end = True
                cogname = 'slowness43'
                return redirect(url_for("absent"))
            else:
                return redirect(url_for("absent"))
        else:
            return render_template("slowness43.html", message=message, pagenum=session['pagenum'])
    return render_template("slowness43.html", message='', pagenum=session['pagenum'])


@app.route('/absent', methods=['post', 'get'])
def absent():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        absentf = request.form.get("absentf")
        absents = request.form.get("absents")
        if absentf is not None and absents is not None:
            session["absentf"] = absentf
            session["absents"] = absents
            session['pagenum'] += 1
            if int(session["absentf"]) >= 0 and int(session["absents"]) >= 0:
                session['cogscoref'] = int(absentf)
                session['cogscores'] = int(absents)
                session['cogscore'] = (int(session['absentf']) + int(session['absents'])) / 2
                # end = True
                cogname = 'absent44'
                return redirect(url_for("bladder"))
        else:
            return render_template("absent44.html", message=message, pagenum=session['pagenum'])
    return render_template("absent44.html", message='', pagenum=session['pagenum'])


@app.route('/bladder', methods=['post', 'get'])
def bladder():
    global end
    form = FlaskForm()
    if request.method == "POST":
        bladderf = request.form.get("bladderf")
        bladders = request.form.get("bladders")
        if bladderf is not None and bladders is not None:
            session["bladderf"] = bladderf
            session["bladders"] = bladders
            session['pagenum'] += 1
            return redirect(url_for("nausea"))
        else:
            return render_template("bladder45.html", message=message, pagenum=session['pagenum'])
    return render_template("bladder45.html", message='', pagenum=session['pagenum'])


@app.route('/nausea', methods=['post', 'get'])
def nausea():
    global end
    form = FlaskForm()
    if request.method == "POST":
        nauseaf = request.form.get("nauseaf")
        nauseas = request.form.get("nauseas")
        if nauseaf is not None and nauseas is not None:
            session["nauseaf"] = nauseaf
            session["nauseas"] = nauseas
            session['pagenum'] += 1
            return redirect(url_for("shortness"))
        else:
            return render_template("nausea47.html", message=message, pagenum=session['pagenum'])
    return render_template("nausea47.html", message='', pagenum=session['pagenum'])


@app.route('/shortness', methods=['post', 'get'])
def shortness():
    global end
    form = FlaskForm()
    if request.method == "POST":
        shortf = request.form.get("shortf")
        shorts = request.form.get("shorts")
        if shortf is not None and shorts is not None:
            session["shortf"] = shortf
            session["shorts"] = shorts
            session['pagenum'] += 1
            return redirect(url_for("dizzy"))
        else:
            return render_template("shortness49.html", message=message, pagenum=session['pagenum'])
    return render_template("shortness49.html", message='', pagenum=session['pagenum'])


@app.route('/dizzy', methods=['post', 'get'])
def dizzy():
    global end
    form = FlaskForm()
    if request.method == "POST":
        dizzyf = request.form.get("dizzyf")
        dizzys = request.form.get("dizzys")
        if dizzyf is not None and dizzys is not None:
            session["dizzyf"] = dizzyf
            session["dizzys"] = dizzys
            session['pagenum'] += 1
            return redirect(url_for("heart"))
        else:
            return render_template("dizzy50.html", message=message, pagenum=session['pagenum'])
    return render_template("dizzy50.html", message='', pagenum=session['pagenum'])


@app.route('/heart', methods=['post', 'get'])
def heart():
    global end
    form = FlaskForm()
    if request.method == "POST":
        heartf = request.form.get("heartf")
        hearts = request.form.get("hearts")
        if heartf is not None and hearts is not None:
            session["heartf"] = heartf
            session["hearts"] = hearts
            session['pagenum'] += 1
            return redirect(url_for("weight"))
        else:
            return render_template("heart51.html", message=message, pagenum=session['pagenum'])
    return render_template("heart51.html", message='', pagenum=session['pagenum'])


@app.route('/weight', methods=['post', 'get'])
def weight():
    global end
    form = FlaskForm()
    if request.method == "POST":
        weightf = request.form.get("weightf")
        weights = request.form.get("weights")
        if weightf is not None and weights is not None:
            session["weightf"] = weightf
            session["weights"] = weights
            session['pagenum'] += 1
            return redirect(url_for("appetite"))
        else:
            return render_template("weight52.html", message=message, pagenum=session['pagenum'])
    return render_template("weight52.html", message='', pagenum=session['pagenum'])


@app.route('/appetite', methods=['post', 'get'])
def appetite():
    global end
    form = FlaskForm()
    if request.method == "POST":
        appetitef = request.form.get("appetitef")
        appetites = request.form.get("appetites")
        if appetitef is not None and appetites is not None:
            session["appetitef"] = appetitef
            session["appetites"] = appetites
            session['pagenum'] += 1
            return redirect(url_for("sweating"))
        else:
            return render_template("appetite53.html", message=message, pagenum=session['pagenum'])
    return render_template("appetite53.html", message='', pagenum=session['pagenum'])


@app.route('/sweating', methods=['post', 'get'])
def sweating():
    global end
    form = FlaskForm()
    if request.method == "POST":
        sweatf = request.form.get("sweatf")
        sweats = request.form.get("sweats")
        if sweatf is not None and sweats is not None:
            session["sweatf"] = sweatf
            session["sweats"] = sweats
            session['pagenum'] += 1
            return redirect(url_for("night"))
        else:
            return render_template("sweating54.html", message=message, pagenum=session['pagenum'])
    return render_template("sweating54.html", message='', pagenum=session['pagenum'])


@app.route('/night', methods=['post', 'get'])
def night():
    global end
    form = FlaskForm()
    if request.method == "POST":
        nightf = request.form.get("nightf")
        nights = request.form.get("nights")
        if nightf is not None and nights is not None:
            session["nightf"] = nightf
            session["nights"] = nights
            session['pagenum'] += 1
            return redirect(url_for("chills"))
        else:
            return render_template("night55.html", message=message, pagenum=session['pagenum'])
    return render_template("night55.html", message='', pagenum=session['pagenum'])


@app.route('/chills', methods=['post', 'get'])
def chills():
    global end
    form = FlaskForm()
    if request.method == "POST":
        chillsf = request.form.get("chillsf")
        chillss = request.form.get("chillss")
        if chillsf is not None and chillss is not None:
            session["chillsf"] = chillsf
            session["chillss"] = chillss
            session['pagenum'] += 1
            return redirect(url_for("hitemp"))
        else:
            return render_template("chills57.html", message=message, pagenum=session['pagenum'])
    return render_template("chills57.html", message='', pagenum=session['pagenum'])


@app.route('/59', methods=['post', 'get'])
def hitemp():
    global end

    form = FlaskForm()
    if request.method == "POST":
        hitempf = request.form.get("hitempf")
        hitemps = request.form.get("hitemps")
        if hitempf is not None and chills is not None:
            session["hitempf"] = hitempf
            session["hitemps"] = hitemps
            session['pagenum'] += 1
            return redirect(url_for("lotemp"))
        else:
            return render_template("hitemp59.html", message=message, pagenum=session['pagenum'])
    return render_template("hitemp59.html", message='', pagenum=session['pagenum'])


@app.route('/60', methods=['post', 'get'])
def lotemp():
    global end

    form = FlaskForm()
    if request.method == "POST":
        lotempf = request.form.get("lotempf")
        lotemps = request.form.get("lotemps")
        if lotempf is not None and lotemps is not None:
            session["lotempf"] = lotempf
            session["lotemps"] = lotemps
            session['pagenum'] += 1
            return redirect(url_for("alcohol"))
        else:
            return render_template("lotemp60.html", message=message, pagenum=session['pagenum'])
    return render_template("lotemp60.html", message='', pagenum=session['pagenum'])


@app.route('/61', methods=['post', 'get'])
def alcohol():
    global end

    form = FlaskForm()
    if request.method == "POST":
        alcoholf = request.form.get("alcoholf")
        alcohols = request.form.get("alcohols")
        if alcoholf is not None and alcohols is not None:
            session["alcoholf"] = alcoholf
            session["alcohols"] = alcohols
            session['pagenum'] += 1
            return redirect(url_for("throat"))
        else:
            return render_template("alcohol61.html", message=message, pagenum=session['pagenum'])
    return render_template("alcohol61.html", message='', pagenum=session['pagenum'])


@app.route('/62', methods=['post', 'get'])
def throat():
    global end
    form = FlaskForm()
    if request.method == "POST":
        throatf = request.form.get("throatf")
        throats = request.form.get("throats")
        if throatf is not None and throats is not None:
            session["throatf"] = throatf
            session["throats"] = throats
            session['pagenum'] += 1
            return redirect(url_for("lymphnodes"))
        else:
            return render_template("throat62.html", message=message, pagenum=session['pagenum'])
    return render_template("throat62.html", message='', pagenum=session['pagenum'])


@app.route('/63', methods=['post', 'get'])
def lymphnodes():
    global end
    form = FlaskForm()
    if request.method == "POST":
        lymphnodesf = request.form.get("lymphnodesf")
        lymphnodess = request.form.get("lymphnodess")
        if lymphnodesf is not None and lymphnodess is not None:
            session["lymphnodesf"] = lymphnodesf
            session["lymphnodess"] = lymphnodess
            session['pagenum'] += 1
            return redirect(url_for("fever"))
        else:
            return render_template("lymphnodes63.html", message=message, pagenum=session['pagenum'])
    return render_template("lymphnodes63.html", message='', pagenum=session['pagenum'])


@app.route('/64', methods=['post', 'get'])
def fever():
    global end
    form = FlaskForm()
    if request.method == "POST":
        feverf = request.form.get("feverf")
        fevers = request.form.get("fevers")
        if feverf is not None and fevers is not None:
            session["feverf"] = feverf
            session["fevers"] = fevers
            session['pagenum'] += 1
            return diagnose2()
        else:
            return render_template("fever64.html", message=message, pagenum=session['pagenum'])
    return render_template("fever64.html", message='', pagenum=session['pagenum'])


@app.route('/vision', methods=['post', 'get'])
def vision():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        visionf = request.form.get("visionf")
        visions = request.form.get("visions")
        if visionf is not None and visions is not None:
            session["visionf"] = visionf
            session["visions"] = visions
            session['pagenum'] += 1
            if int(session["visionf"]) >= 0 and int(session["visions"]) >= 0:
                session['cogscoref'] = int(visionf)
                session['cogscores'] = int(visions)
                session['cogscore'] = (int(session['visionf']) + int(session['visions'])) / 2
                # end = True
                cogname = 'unable41'
                return redirect(url_for('depth'))

        else:
            return render_template("vision41.html", message=message, pagenum=session['pagenum'])
    return render_template("vision41.html", message='', pagenum=session['pagenum'])


@app.route('/depth', methods=['post', 'get'])
def depth():
    global end
    form = FlaskForm()
    if request.method == "POST":
        depthf = request.form.get("depthf")
        depths = request.form.get("depths")
        if depthf is not None and depths is not None:
            session["depthf"] = depthf
            session["depths"] = depths
            session['pagenum'] += 1
            return redirect(url_for("slowness"))
        else:
            return render_template("depth42.html", message=message, pagenum=session['pagenum'])
    return render_template("depth42.html", message='', pagenum=session['pagenum'])


@app.route('/musclepain', methods=['post', 'get'])
def musclepain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        musclef = request.form.get("musclef")
        mucles = request.form.get("muscles")
        if musclef is not None and mucles is not None:
            session["musclef"] = musclef
            session["muscles"] = mucles
            session['pagenum'] += 1
            return redirect(url_for("bloating"))
        else:
            return render_template("musclepain.html", message=message, pagenum=session['pagenum'])
    return render_template("musclepain.html", message='', pagenum=session['pagenum'])


@app.route('/bloating', methods=['post', 'get'])
def bloating():
    global end
    form = FlaskForm()
    if request.method == "POST":
        bloatf = request.form.get("bloatf")
        bloats = request.form.get("bloats")
        if bloats is not None and bloatf is not None:
            session["bloatf"] = bloatf
            session["bloats"] = bloats
            session['pagenum'] += 1
            return redirect(url_for("bowel"))
        else:
            return render_template("bloating.html", message=message, pagenum=session['pagenum'])
    return render_template("bloating.html", message='', pagenum=session['pagenum'])


@app.route('/bowel', methods=['post', 'get'])
def bowel():
    global end
    form = FlaskForm()
    if request.method == "POST":
        bowelf = request.form.get("bowelf")
        bowels = request.form.get("bowels")
        if bowels is not None and bowelf is not None:
            session["bowelf"] = bowelf
            session["bowels"] = bowels
            session['pagenum'] += 1
            return redirect(url_for("unsteady"))
        else:
            return render_template("bowel.html", message=message, pagenum=session['pagenum'])
    return render_template("bowel.html", message='', pagenum=session['pagenum'])


@app.route('/unsteady', methods=['post', 'get'])
def unsteady():
    global end
    form = FlaskForm()
    if request.method == "POST":
        unsteadyf = request.form.get("unsteadyf")
        unsteadys = request.form.get("unsteadys")
        if unsteadyf is not None and unsteadys is not None:
            session["unsteadyf"] = unsteadyf
            session["unsteadys"] = unsteadys
            session['pagenum'] += 1
            return redirect(url_for("cold_limbs"))
        else:
            return render_template("unsteady.html", message=message, pagenum=session['pagenum'])
    return render_template("unsteady.html", message='', pagenum=session['pagenum'])


@app.route('/cold_limbs', methods=['post', 'get'])
def cold_limbs():
    global end
    form = FlaskForm()
    if request.method == "POST":
        limbsf = request.form.get("limbsf")
        limbss = request.form.get("limbss")
        if limbsf is not None and limbss is not None:
            session["limbsf"] = limbsf
            session["limbss"] = limbss
            session['pagenum'] += 1
            return redirect(url_for("hot_cold"))
        else:
            return render_template("limbs.html", message=message, pagenum=session['pagenum'])
    return render_template("limbs.html", message='', pagenum=session['pagenum'])


@app.route('/hot_cold', methods=['post', 'get'])
def hot_cold():
    global end
    form = FlaskForm()
    if request.method == "POST":
        hotf = request.form.get("hotf")
        hots = request.form.get("hots")
        if hotf is not None and hots is not None:
            session["hotf"] = hotf
            session["hots"] = hots
            session['pagenum'] += 1
            return redirect(url_for("flu"))
        else:
            return render_template("hot.html", message=message, pagenum=session['pagenum'])
    return render_template("hot.html", message='', pagenum=session['pagenum'])


@app.route('/flu', methods=['post', 'get'])
def flu():
    global end
    form = FlaskForm()
    if request.method == "POST":
        fluf = request.form.get("fluf")
        flus = request.form.get("flus")
        if fluf is not None and flus is not None:
            session["fluf"] = fluf
            session["flus"] = flus
            session['pagenum'] += 1
            return redirect(url_for("smells"))
        else:
            return render_template("flu.html", message=message, pagenum=session['pagenum'])
    return render_template("flu.html", message='', pagenum=session['pagenum'])


@app.route('/smells', methods=['post', 'get'])
def smells():
    global end
    global survey
    form = FlaskForm()
    if request.method == "POST":
        smellf = request.form.get("smellf")
        smells = request.form.get("smells")
        if smellf is not None and smells is not None:
            session["smellf"] = smellf
            session["smells"] = smells
            session['pagenum'] += 1
            survey = 'rf14'
            return diagnose()
        else:
            return render_template("smells.html", message=message, pagenum=session['pagenum'])
    return render_template("smells.html", message='', pagenum=session['pagenum'])


@app.route('/reduction', methods=['post', 'get'])
def reduction():
    msg_reduction = "Please select one of the options before continuing"
    if request.method == 'POST':
        reduction = request.form.get('reduction')
        if reduction is not None:
            session['reduction'] = reduction
            return diagnose()
        else:
            return render_template("reduction.html", message=msg_reduction, pagenum=session['pagenum'])
    return render_template('reduction.html', message='', pagenum=session['pagenum'])


@app.route('/end', methods=['post', 'get'])
def end():
    form = FlaskForm()
    if request.method == "POST":
        return redirect(url_for('home'))
    # return render_template("example4.html")

    if end:
        fatiguedata = ((int(session["fatiguescoref"]) + int(session['fatiguescores'])) / 2)
        minexdata = ((int(session["minexf"]) + int(session['minexs'])) / 2)
        sleepdata = ((int(session["sleepf"]) + int(session['sleeps'])) / 2)
        cogdata = ((int(session["rememberf"]) + int(session['remembers'])) / 2)
        # data = [fatiguedata, minexdata, sleepdata, cogdata]
        data = np.array([[fatiguedata, minexdata, sleepdata, cogdata]])
        # result = randomForest.rf2.predict(data)
        # if result[0] == 1:
        # return f"The random forest model classifies your responses with the ME/CFS group. Model accuracy is {randomForest.accuracy}"
        # else:
        # return f"The random forest model does not predict ME/CFS. Model accuracy is {randomForest.accuracy}"

        # return f"{result}"


@app.route('/about', methods=['post', 'get'])
def about():
    return render_template('about.html')


@app.route('/aboutmecfs', methods=['post', 'get'])
def aboutmecfs():
    return render_template('aboutmecfs.html')


if __name__ == '__main__':
    app.run(debug=True)
