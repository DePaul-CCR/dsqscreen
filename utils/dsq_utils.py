from flask import render_template, session
import numpy as np
import plotly.graph_objects as go
import json
import plotly.utils
from utils.general_utils import get_score
import utils.domainScores as ds
# see dsqitems_and_routes_map.txt for info on each section of the screener

def dsq_diagnose():
    # IOM assessment
    iomfatiguecheck = "No"
    iomreductioncheck = "No"
    iompemcheck = "No"
    iomsleepcheck = "No"
    iomcogcheck = "No"
    iomorthocheck = "No"

    if get_score('fatiguescoref') >= 2 and get_score('fatiguescores') >= 2:
        iomfatiguecheck = "Yes"

    if get_score('reduction') == 1:
        iomreductioncheck = "Yes"

    if (get_score('minexf') >= 2 and get_score('minexs') >= 2) or (
        get_score('heavyf') >= 2 and get_score('heavys') >= 2) or (
        get_score('soref') >= 2 and get_score('sores') >= 2) or (
        get_score('mentalf') >= 2 and get_score('mentals') >= 2) or (
        get_score('drainedf') >= 2 and get_score('draineds') >= 2):
        iompemcheck = "Yes"

    if (get_score('sleepf') >= 2 and get_score('sleeps') >= 2) or (
        get_score('napf') >= 2 and get_score('naps') >= 2) or (
        get_score('fallf') >= 2 and get_score('falls') >= 2) or (
        get_score('stayf') >= 2 and get_score('stays') >= 2) or (
        get_score('alldayf') >= 2 and get_score('alldays') >= 2):
        iomsleepcheck = "Yes"

    if (get_score('lightsf') >= 2 and get_score('lightss') >= 2) or (
        get_score('rememberf') >= 2 and get_score('remembers') >= 2) or (
        get_score('attentionf') >= 2 and get_score('attentions') >= 2) or (
        get_score('wordf') >= 2 and get_score('words') >= 2) or (
        get_score('understandf') >= 2 and get_score('understands') >= 2) or (
        get_score('focusf') >= 2 and get_score('focuss') >= 2) or (
        get_score('visionf') >= 2 and get_score('visions') >= 2) or (
        get_score('depthf') >= 2 and get_score('depths') >= 2) or (
        get_score('slowf') >= 2 and get_score('slows') >= 2) or (
        get_score('absentf') >= 2 and get_score('absents') >= 2):
        iomcogcheck = "Yes"

    if (get_score('unsteadyf') >= 2 and get_score('unsteadys') >= 2) or (
        get_score('shortf') >= 2 and get_score('shorts') >= 2) or (
        get_score('dizzyf') >= 2 and get_score('dizzys') >= 2) or (
        get_score('heartf') >= 2 and get_score('hearts') >= 2):
        iomorthocheck = "Yes"

    if iomfatiguecheck == "Yes" and iomreductioncheck == "Yes" and iompemcheck == "Yes" and iomsleepcheck == "Yes" and (iomcogcheck == "Yes" or iomorthocheck == "Yes"):
        iom_msg = "Your responses suggest you meet the IOM Criteria for ME/CFS."
        iomdxcheck = "Met"
    else:
        iom_msg = "Your responses do not meet the IOM Criteria for ME/CFS."
        iomdxcheck = "Not met"

    # Canadian criteria assessment
    ccc_dx = False

    if get_score('fatiguescoref') >= 2 and get_score('fatiguescores') >= 2:
        ccc_fatigue = 1
        ccc_fatiguecheck = "Yes"
    else:
        ccc_fatigue = 0
        ccc_fatiguecheck = "No"

    if get_score('reduction') == 1:
        ccc_reduction = 1
        ccc_reductioncheck = "Yes"
    else:
        ccc_reduction = 0
        ccc_reductioncheck = "No"

    if (get_score('musclef') >= 2 and get_score('muscles') >= 2) or (
        get_score('jointpainf') >= 2 and get_score('jointpains') >= 2) or (
        get_score('eyepainf') >= 2 and get_score('eyepains') >= 2) or (
        get_score('chestpainf') >= 2 and get_score('chestpains') >= 2) or (
        get_score('headachesf') >= 2 and get_score('headachess') >= 2) or (
        get_score('bloatf') >= 2 and get_score('bloats') >= 2) or (
        get_score('stomachf') >= 2 and get_score('stomachs') >= 2):
        ccc_pain = 1
        ccc_paincheck = "Yes"
    else:
        ccc_pain = 0
        ccc_paincheck = "No"

    if (get_score('sleepf') >= 2 and get_score('sleeps') >= 2) or (
        get_score('napf') >= 2 and get_score('naps') >= 2) or (
        get_score('fallf') >= 2 and get_score('falls') >= 2) or (
        get_score('stayf') >= 2 and get_score('stays') >= 2) or (
        get_score('earlyf') >= 2 and get_score('earlys') >= 2) or (
        get_score('alldayf') >= 2 and get_score('alldays') >= 2):
        ccc_sleep = 1
        ccc_sleepcheck = "Yes"
    else:
        ccc_sleep = 0
        ccc_sleepcheck = "No"

    if (get_score('heavyf') >= 2 and get_score('heavys') >= 2) or (
        get_score('soref') >= 2 and get_score('sores') >= 2) or (
        get_score('mentalf') >= 2 and get_score('mentals') >= 2) or (
        get_score('minexf') >= 2 and get_score('minexs') >= 2) or (
        get_score('drainedf') >= 2 and get_score('draineds') >= 2):
        ccc_pem = 1
        ccc_pemcheck = "Yes"
    else:
        ccc_pem = 0
        ccc_pemcheck = "No"

    if (get_score('twitchesf') >= 2 and get_score('twitchess') >= 2) or (
        get_score('weakf') >= 2 and get_score('weaks') >= 2) or (
        get_score('noisef') >= 2 and get_score('noises') >= 2) or (
        get_score('lightsf') >= 2 and get_score('lightss') >= 2) or (
        get_score('rememberf') >= 2 and get_score('remembers') >= 2) or (
        get_score('attentionf') >= 2 and get_score('attentions') >= 2) or (
        get_score('wordf') >= 2 and get_score('words') >= 2) or (
        get_score('understandf') >= 2 and get_score('understands') >= 2) or (
        get_score('focusf') >= 2 and get_score('focuss') >= 2) or (
        get_score('visionf') >= 2 and get_score('visions') >= 2) or (
        get_score('depthf') >= 2 and get_score('depths') >= 2) or (
        get_score('slowf') >= 2 and get_score('slows') >= 2) or (
        get_score('absentf') >= 2 and get_score('absents') >= 2):
        ccc_cog = 1
        ccc_cogcheck = "Yes"
    else:
        ccc_cog = 0
        ccc_cogcheck = "No"

    if (get_score('unsteadyf') >= 2 and get_score('unsteadys') >= 2) or (
            get_score('bowelf') >= 2 and get_score('bowels') >= 2) or (
            get_score('bladderf') >= 2 and get_score('bladders') >= 2) or (
            get_score('nauseaf') >= 2 and get_score('nauseas') >= 2) or (
            get_score('shortf') >= 2 and get_score('shorts') >= 2) or (
            get_score('dizzyf') >= 2 and get_score('dizzys') >= 2) or (
            get_score('heartf') >= 2 and get_score('hearts') >= 2):
        ccc_auto = 1
        ccc_autocheck = "Yes"
    else:
        ccc_auto = 0
        ccc_autocheck = "No"

    if (get_score('sweatf') >= 2 and get_score('sweats') >= 2) or (
        get_score('nightf') >= 2 and get_score('nights') >= 2) or (
        get_score('limbsf') >= 2 and get_score('limbss') >= 2) or (
        get_score('chillsf') >= 2 and get_score('chillss') >= 2) or (
        get_score('hotf') >= 2 and get_score('hots') >= 2) or (
        get_score('hitempf') >= 2 and get_score('hitemps') >= 2) or (
        get_score('lotempf') >= 2 and get_score('lotemps') >= 2) or (
        get_score('appetitef') >= 2 and get_score('appetites') >= 2) or (
        get_score('weightf') >= 2 and get_score('weights') >= 2) or (
        get_score('alcoholf') >= 2 and get_score('alcohols') >= 2):
        ccc_neuro = 1
        ccc_neurocheck = "Yes"
    else:
        ccc_neuro = 0
        ccc_neurocheck = "No"

    if (get_score('fluf') >= 2 and get_score('flus') >= 2) or (
        get_score('smellf') >= 2 and get_score('smells') >= 2) or (
        get_score('throatf') >= 2 and get_score('throats') >= 2) or (
        get_score('lymphnodesf') >= 2 and get_score('lymphnodess') >= 2) or (
        get_score('feverf') >= 2 and get_score('fevers') >= 2):
        ccc_immune = 1
        ccc_immunecheck = "Yes"
    else:
        ccc_immune = 0
        ccc_immunecheck = "No"

    ccc_poly = np.sum([ccc_auto, ccc_neuro, ccc_immune])
    # most of the symptoms are required, but there is one polythetic criteria, shown here by ccc_poly
    if np.sum([ccc_fatigue, ccc_reduction, ccc_pem, ccc_sleep, ccc_pain, ccc_cog]) == 6 and ccc_poly >= 2:
        ccc_dx = "Met"
        ccc_msg = "Your responses suggest that you meet the Canadian Consensus Criteria for ME/CFS."
    else:
        ccc_dx = "Not met"
        ccc_msg = "Your responses do not meet the Canadian Consensus Criteria for ME/CFS."
    
    # diagnostic message true if ccc OR iom
    if ccc_dx == "Met" or iomdxcheck == "Met":
        dsq_message = "Based on your responses there is a chance you might have MECFS. <br> Please consult with your doctor for next steps."
    else:
        dsq_message = "Based on your responses it does not appear you have MECFS."

    graphJSON = dsq_graph()

    return render_template("results/graph3.html", graphJSON=graphJSON,
                           ccc_msg=ccc_msg, ccc_fatiguecheck=ccc_fatiguecheck,
                           ccc_pemcheck=ccc_pemcheck, ccc_paincheck=ccc_paincheck, ccc_sleepcheck=ccc_sleepcheck,
                           ccc_cogcheck=ccc_cogcheck, ccc_autocheck=ccc_autocheck, ccc_immunecheck=ccc_immunecheck,
                           ccc_neurocheck=ccc_neurocheck, ccc_dx=ccc_dx, ccc_reductioncheck=ccc_reductioncheck, ccc_poly=ccc_poly,
                           iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                           iompemcheck=iompemcheck, iomdxcheck=iomdxcheck, iom_msg=iom_msg,
                           iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck, iomorthocheck=iomorthocheck, dsq_message=dsq_message)

def dsq_graph():
    fatigue_score = (get_score("fatiguescoref") + get_score("fatiguescores")) / 2

    pem_score = (get_score('heavyf') + get_score('heavys') + get_score('soref') + get_score('sores') +
                 get_score('mentalf') + get_score('mentals') + get_score("minexf") + get_score("minexs") + 
                 get_score('drainedf') + get_score('draineds')) / 10
    
    sleep_score = (get_score("sleepf") + get_score("sleeps") + get_score('napf') + get_score('naps') +
                   get_score('fallf') + get_score('falls') + get_score('stayf') + get_score('stays') +
                   get_score('earlyf') + get_score('earlys') + get_score('alldayf') + get_score('alldays')) / 12
    
    pain_score = (get_score('musclef') + get_score('muscles') + get_score('jointpainf') + get_score('jointpains') + 
                  get_score('eyepainf') + get_score('eyepains') + get_score('chestpainf') + get_score('chestpains') +
                  get_score('bloatf') + get_score('bloats') + get_score('stomachf') + get_score('stomachs') +
                  get_score('headachesf') + get_score('headachess')) / 14
    
    cog_score = (get_score('twitchesf') + get_score('twitchess') + get_score('weakf') + get_score('weaks') + 
                 get_score('noisef') + get_score('noises') + get_score('lightsf') + get_score('lightss') + 
                 get_score("rememberf") + get_score("remembers") + get_score('attentionf') + get_score('attentions') +
                 get_score('wordf') + get_score('words') + get_score('understandf') + get_score('understands') +
                 get_score('focusf') + get_score('focuss') + get_score('visionf') + get_score('visions') +
                 get_score('depthf') + get_score('depths') + get_score('slowf') + get_score('slows') +
                 get_score('absentf') + get_score('absents')) / 26
    
    autonomic_score = (get_score('bladderf') + get_score('bladders') + get_score('bowelf') + get_score('bowels') +
                       get_score('nauseaf') + get_score('nauseas') + get_score('unsteadyf') + get_score('unsteadys') + 
                       get_score('shortf') + get_score('shorts') + get_score('dizzyf') + get_score('dizzys') + 
                       get_score('heartf') + get_score('hearts')) / 14
    
    neuro_score = (get_score('weightf') + get_score('weights') + get_score('appetitef') + get_score('appetites') +
                   get_score('sweatf') + get_score('sweats') + get_score('nightf') + get_score('nights') +
                   get_score('limbsf') + get_score('limbss') + get_score('chillsf') + get_score('chillss') +
                   get_score('hotf') + get_score('hots') + get_score('hitempf') + get_score('hitemps') +
                   get_score('lotempf') + get_score('lotemps') + get_score('alcoholf') + get_score('alcohols')) / 20
    
    immune_score = (get_score('throatf') + get_score('throats') + get_score('lymphnodesf') + get_score('lymphnodess') +
                    get_score('feverf') + get_score('fevers') + get_score('fluf') + get_score('flus') +
                    get_score('smellf') + get_score('smells')) / 10

    # Not currently using control data - PC 09/5/23
    # control = ds.df[(ds.df['dx'] != 1)]
    # conDomains = np.mean(control.iloc[:, 110:120], axis=0)
    mecfs = ds.df[(ds.df['dx'] == 1)]
    cfsdomains = np.mean(mecfs.iloc[:, 110:118], axis=0)
    user_scores = [fatigue_score, pem_score, sleep_score, pain_score, cog_score, autonomic_score, neuro_score, immune_score]

    categories = ['Fatigue', 'PEM', 'Sleep Issues', 'Pain', 'Cognitive Problems', 'Autonomic Problems', 'Neurological Problems', 'Immune System']

    # converts scores to 100pt scale
    user_scores = np.multiply(user_scores, 25).tolist()
    cfsdomains = np.multiply(cfsdomains, 25).tolist()
    
    fig = go.Figure(
        data=[
            go.Bar(y=user_scores, x=categories, name="Your scores", marker_color='#00CC9C'),
            go.Bar(y=cfsdomains, x=categories, name="Average ME/CFS scores", marker_color='#1E3888')],
        layout=go.Layout(
            title=go.layout.Title(text='Your scores compared with our dataset of <br>'
                                       'over 2,400 participants with ME/CFS', x=0.5),
            showlegend=True, legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1)))
    fig.update_layout(yaxis_title='Averaged Frequency and Severity Scores',
                      xaxis_title='Symptom Domains')
    fig.update_yaxes(range=[0, 100], dtick=25)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)