from flask import render_template, session
import numpy as np
import plotly.graph_objects as go
import json
import plotly.utils
import utils.domainScores as ds
from utils.general_utils import get_score
from utils.export_columns_util import build_dataframe_for_export, dump_collected_data_to_sheet
# see dsqitems_and_routes_map.txt for info on each section of the screener

def short_form_diagnose():
    #Assesses the IOM Criteria
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
            get_score('soref') >= 2 and get_score('sores') >= 2):
        iompemcheck = "Yes"

    if get_score('sleepf') >= 2 and get_score('sleeps') >= 2:
        iomsleepcheck = "Yes"

    if (get_score('rememberf') >= 2 and get_score('remembers') >= 2) or (
            get_score('attentionf') >= 2 and get_score('attentions') >= 2):
        iomcogcheck = "Yes"

    if get_score('unsteadyf') >= 2 and get_score('unsteadys') >= 2:
        iomorthocheck = "Yes"

    if iomfatiguecheck == "Yes" and iomreductioncheck == "Yes" and iompemcheck == "Yes" and iomsleepcheck == "Yes" and (iomcogcheck == "Yes" or iomorthocheck == "Yes"):
        iom_msg = "Your responses suggest you meet the IOM criteria for ME/CFS. To improve the accuracy" \
                  " of your assessment with more questions continue to the next section."
        iomdxcheck = "Met"
    else:
        iom_msg = "Your responses do not meet the IOM criteria for ME/CFS."
        iomdxcheck = "Not met"

    # This assesses the Canadian Consensus Criteria, one of the three major case definitions we use
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
    
    if (get_score('minexf') >= 2 and get_score('minexs') >= 2) or (
        get_score('soref') >= 2 and get_score('sores') >= 2):
        ccc_pem = 1
        ccc_pemcheck = "Yes"
    else:
        ccc_pem = 0
        ccc_pemcheck = "No"
    
    if (get_score('rememberf') >= 2 and get_score('remembers') >= 2) or (
        get_score('attentionf') >= 2 and get_score('attentions') >= 2):
        ccc_cog = 1
        ccc_cogcheck = "Yes"
    else:
        ccc_cog = 0
        ccc_cogcheck = "No"

    if get_score('musclef') >= 2 and get_score('muscles') >= 2 or (
       get_score('bloatf') >= 2 and get_score('bloats') >= 2):
        ccc_pain = 1
        ccc_paincheck = "Yes"
    else:
        ccc_pain = 0
        ccc_paincheck = "No"
    
    if (get_score('unsteadyf') >= 2 and get_score('unsteadys') >= 2) or (
        get_score('bowelf') >= 2 and get_score('bowels') >= 2):
        ccc_auto = 1
        ccc_autocheck = "Yes"
    else:
        ccc_auto = 0
        ccc_autocheck = "No"
    
    if (get_score('limbsf') >= 2 and get_score('limbss') >= 2) or (
        get_score('hotf') >= 2 and get_score('hots') >= 2):
        ccc_neuro = 1
        ccc_neurocheck = "Yes"
    else:
        ccc_neuro = 0
        ccc_neurocheck = "No"
    
    if (get_score('fluf') >= 2 and get_score('flus') >= 2) or (
        get_score('smellf') >= 2 and get_score('smells') >= 2):
        ccc_immune = 1
        ccc_immunecheck = "Yes"
    else:
        ccc_immune = 0
        ccc_immunecheck = "No"

    if get_score('sleepf') >= 2 and get_score('sleeps') >= 2:
        ccc_sleep = 1
        ccc_sleepcheck = "Yes"
    else:
        ccc_sleep = 0
        ccc_sleepcheck = "No"
    
    ccc_poly = np.sum([ccc_auto, ccc_neuro, ccc_immune, ccc_pain])
    # most of the domains are required, but there is one polythetic criteria, shown here by ccc_poly
    if np.sum([ccc_fatigue, ccc_reduction, ccc_pem, ccc_sleep, ccc_cog]) == 5 and ccc_poly >= 1:
        ccc_dx = "Met"
        ccc_msg = "Your responses suggest that you meet the Canadian Consensus Criteria for ME/CFS. " \
                  "To improve the accuracy of your assessment with more questions continue to the next section."
    else:
        ccc_dx = "Not met"
        ccc_msg = "Your responses do not meet the Canadian Consensus Criteria for ME/CFS."

    # diagnostic message ccc OR iom
    dx_met = False
    if ccc_dx == "Met" or iomdxcheck == "Met":
        short_form_message = "Based on your responses there is a chance you might have MECFS. <br> Please continue to the next section for a more accurate assessment."
        dx_met = True
    else:
        short_form_message = "Based on your responses it does not appear you have MECFS."

    graphJSON = short_form_graph()

    # dump to Google Sheets [Disabled until approved & needed -PC 7/26/24]
    # df = build_dataframe_for_export(session, "short_form")
    # dump_collected_data_to_sheet(df)

    return render_template("results/graph2.html", graphJSON=graphJSON, ccc_msg=ccc_msg, ccc_fatiguecheck=ccc_fatiguecheck,
                           ccc_pemcheck=ccc_pemcheck, ccc_paincheck=ccc_paincheck, ccc_sleepcheck=ccc_sleepcheck,
                           ccc_cogcheck=ccc_cogcheck, ccc_autocheck=ccc_autocheck, ccc_immunecheck=ccc_immunecheck,
                           ccc_neurocheck=ccc_neurocheck, ccc_dx=ccc_dx, ccc_reductioncheck=ccc_reductioncheck, ccc_poly=ccc_poly,
                           iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                           iompemcheck=iompemcheck, iomdxcheck=iomdxcheck, iom_msg=iom_msg,
                           iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck, iomorthocheck=iomorthocheck,
                           short_form_message=short_form_message,dx_met=dx_met
                           )

def short_form_graph():
    # we use CCC domains / DSQSF scoring for placing items in this bar chart
    fatigue_score = (get_score("fatiguescoref") + get_score("fatiguescores")) / 2
    pem_score = (get_score("minexf") + get_score("minexs") + get_score('soref') + get_score('sores')) / 4
    sleep_score = (get_score("sleepf") + get_score("sleeps")) / 2
    pain_score = (get_score('musclef') + get_score('muscles') + get_score('bloatf') + get_score('bloats')) / 4
    cog_score = (get_score("rememberf") + get_score("remembers") + get_score('attentionf') + get_score('attentions')) / 4
    autonomic_score = (get_score('unsteadyf') + get_score('unsteadys') + get_score('bowelf') + get_score('bowels')) / 4
    neuro_score = (get_score('limbsf') + get_score('limbss') + get_score('hotf') + get_score('hots')) / 4
    immune_score = (get_score('fluf') + get_score('flus') + get_score('smellf') + get_score('smells')) / 4

    user_scores = [fatigue_score, pem_score, sleep_score, pain_score, cog_score, autonomic_score, neuro_score, immune_score]
    categories = ['Fatigue', 'PEM', 'Sleep Issues', 'Pain', 'Cognitive Problems', 'Autonomic Problems', 'Neurological Problems', 'Immune System']

    df = ds.sdf
    mecfs = df[(df['dx'] == 1)]
    # takes the symptom domain score means calculated in domainScores.py
    cfsdomains = np.mean(mecfs.iloc[:, 110:118], axis=0)

    # converts scores to 100pt scale for chart
    user_scores = np.multiply(user_scores, 25).tolist()
    cfsdomains = np.multiply(cfsdomains, 25).tolist()

    # Creates a figure using the plotly library, which can be dynamically embedded in the HTML page
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
    # This converts to figure fig to a JSON object so it can be dynamically rendered with javascript on the page
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)