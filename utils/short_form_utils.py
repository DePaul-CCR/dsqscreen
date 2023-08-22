from flask import render_template, session
import numpy as np
import plotly.graph_objects as go
import json
import plotly.utils

# short form questions:
# soreness15c, difficulty37c, musclepain25c, bloating29c,
# bowel46c, unsteady48c, limbs56c, hot58c, flu65c, smells66c, reduction97
# includes screener qs: (fatigue13c, minimum17c, unrefreshed19c, remember36c)

def short_form_diagnose():
    import domainScores as ds

    fatiguescore = (int(session["fatiguescoref"]) + int(session["fatiguescores"])) / 2
    pemscore = (int(session["minexf"]) + int(session["minexs"]) + int(session['soref']) + int(session['sores'])) / 4
    sleepscore = (int(session["sleepf"]) + int(session["sleeps"])) / 2
    cogscore = (int(session["rememberf"]) + int(session["remembers"]) + int(session['attentionf']) +
                int(session['attentions'])) / 4
    painscore = (int(session['musclef']) + int(session['muscles'])) / 2
    gastroscore = (int(session['bloatf']) + int(session['bloats']) + int(session['bowelf']) +
                   int(session['bowels'])) / 4
    orthoscore = (int(session['unsteadyf']) + int(session['unsteadys'])) / 2
    circscore = (int(session['limbsf']) + int(session['limbss']) + int(session['hotf']) + int(session['hots'])) / 4
    immunescore = (int(session['fluf']) + int(session['flus'])) / 2
    neuroenscore = (int(session['smellf']) + int(session['smells'])) / 2

    user_scores = [fatiguescore, pemscore, sleepscore, cogscore, painscore, gastroscore, orthoscore, circscore,
                   immunescore, neuroenscore]

    df = ds.sdf
    mecfs = df[(df['dx'] == 1)]
    cfsdomains = np.mean(mecfs.iloc[:, 110:120], axis=0)

    # This assesses the IOM Criteria
    responses = [fatiguescore, pemscore, sleepscore, cogscore]
    iomfatiguecheck = "No"
    iomreductioncheck = "No"
    iompemcheck = "No"
    iomsleepcheck = "No"
    iomcogcheck = "No"
    iomorthocheck = "No"

    if int(session['fatiguescoref']) >= 2 and int(session['fatiguescores']) >= 2:
        iomfatiguecheck = "Yes"
    if int(session['reduction']) == 1:
        iomreductioncheck = "Yes"
    if (int(session['minexf']) >= 2 and int(session['minexs'] >= 2) or (
            int(session['soref']) >= 2 and int(session['sores']) >= 2)):
        iompemcheck = "Yes"
    if int(session['sleepf']) >= 2 and int(session['sleeps']) >= 2:
        iomsleepcheck = "Yes"
    if (int(session['rememberf']) >= 2 and int(session['remembers']) >= 2 ) or (
            int(session['attentionf']) >= 2 and int(session['attentions']) >= 2):
        iomcogcheck = "Yes"
    if int(session['unsteadyf']) >= 2 and int(session['unsteadys']) >= 2:
        iomorthocheck = "Yes"

    if iomfatiguecheck == "Yes" and iomreductioncheck == "Yes" and iompemcheck == "Yes" and iomsleepcheck == "Yes" and (iomcogcheck == "Yes" or iomorthocheck == "Yes"):
        iom_msg = "Your responses suggest you meet the IOM Criteria for ME/CFS. To improve the accuracy" \
                  " of your assessment with more questions continue to the next section."
        iomdxcheck = "Met"

    else:
        iom_msg = "Your responses do not meet the IOM Criteria for ME/CFS."
        iomdxcheck = "Not met"

    # This assesses the Canadian Consensus Criteria, one of the three major case definitions we use

    ccc_dx = False

    if int(session['fatiguescoref']) >= 2 and int(session['fatiguescores']) >= 2:
        ccc_fatigue = 1
        ccc_fatiguecheck = "Yes"
    else:
        ccc_fatigue = 0
        ccc_fatiguecheck = "No"
    if int(session['reduction']) == 1:
        ccc_reduction = 1
        ccc_reductioncheck = "Yes"
    else:
        ccc_reduction = 0
        ccc_reductioncheck = "No"
    if int(session['musclef']) >= 2 and int(session['muscles']) >= 2:
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
    if (int(session['rememberf']) >= 2 and int(session['remembers']) >= 2) or (
            int(session['attentionf']) >= 2 and int(session['attentions']) >= 2):
        ccc_cog = 1
        ccc_cogcheck = "Yes"
    else:
        ccc_cog = 0
        ccc_cogcheck = "No"

    if (int(session['unsteadyf']) >= 2 and int(session['unsteadys']) >= 2) or (
            int(session['bowelf']) >= 2 and int(session['bowels']) >= 2) or (
            int(session['bloatf']) >= 2 and int(session['bloats']) >= 2):
        ccc_auto = 1
        ccc_autocheck = "Yes"
    else:
        ccc_auto = 0
        ccc_autocheck = "No"
    if (int(session['limbsf']) >= 2 and int(session['limbss']) >= 2) or (
            int(session['hotf']) >= 2 and int(session['hots']) >= 2):
        ccc_neuro = 1
        ccc_neurocheck = "Yes"
    else:
        ccc_neuro = 0
        ccc_neurocheck = "No"
    if (int(session['fluf']) >= 2 and int(session['flus']) >= 2) or (
            int(session['smellf']) >= 2 and int(session['smells']) >= 2):
        ccc_immune = 1
        ccc_immunecheck = "Yes"
    else:
        ccc_immune = 0
        ccc_immunecheck = "No"
    ccc_poly = np.sum([ccc_auto, ccc_neuro, ccc_immune])
    # most of the symptoms are required, but there is one polythetic criteria, shown here by ccc_poly
    if np.sum([ccc_fatigue, ccc_reduction, ccc_pem, ccc_sleep, ccc_pain, ccc_cog]) >= 6 and ccc_poly >= 2:
        ccc_dx = "Met"
        ccc_msg = "Your responses suggest that you meet the Canadian Consensus Criteria for ME/CFS. " \
                  "To improve the accuracy of your assessment with more questions continue to the next section."
    else:
        ccc_dx = "Not met"
        ccc_msg = "Your responses do not meet the Canadian Consensus Criteria for ME/CFS."

    # categories = [*feature_list, feature_list[0]]
    categories = ['Fatigue', 'PEM', 'Sleep', 'Cognitive Impairment', 'Pain', 'Gastro Problems',
                  'Orthostatic Intolerance', 'Circulatory Problems', 'Immune System', 'Neuroendocrine Problems']

    # converts scores to 100pt scale
    user_scores = np.multiply(user_scores, 25).tolist()
    cfsdomains = np.multiply(cfsdomains, 25).tolist()

    # diagnostic message ccc OR iom
    dx_met = False
    if ccc_dx == "Met" or iomdxcheck == "Met":
        short_form_message = "Based on your responses there is a chance you might have MECFS. <br> Please continue to the next section for a more accurate assessment."
        dx_met = True
    else:
        short_form_message = "Based on your responses it does not appear you have MECFS."

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
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("results/graph2.html", graphJSON=graphJSON, ccc_msg=ccc_msg, ccc_fatiguecheck=ccc_fatiguecheck,
                           ccc_pemcheck=ccc_pemcheck, ccc_paincheck=ccc_paincheck, ccc_sleepcheck=ccc_sleepcheck,
                           ccc_cogcheck=ccc_cogcheck, ccc_autocheck=ccc_autocheck, ccc_immunecheck=ccc_immunecheck,
                           ccc_neurocheck=ccc_neurocheck, ccc_dx=ccc_dx, ccc_reductioncheck=ccc_reductioncheck, ccc_poly=ccc_poly,
                           iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                           iompemcheck=iompemcheck, iomdxcheck=iomdxcheck, iom_msg=iom_msg,
                           iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck, iomorthocheck=iomorthocheck,
                           short_form_message=short_form_message,dx_met=dx_met
                           )