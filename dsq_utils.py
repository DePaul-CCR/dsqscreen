from flask import render_template, session
import numpy as np
import plotly.graph_objects as go
import json
import plotly.utils

def dsq_diagnose():
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
    cfsdomains = np.mean(mecfs.iloc[:, 110:120], axis=0)
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
    
    # converts scores to 100pt scale
    user_scores = np.multiply(user_scores, 25).tolist()
    cfsdomains = np.multiply(cfsdomains, 25).tolist()
    
    fig = go.Figure(
        data=[
            go.Bar(y=user_scores, x=categories, name="Your scores"),
            go.Bar(y=cfsdomains, x=categories, name="Average ME/CFS scores")],
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
    fig.add_hline(y=1.5 * 25, line_color='black')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("results/graph3.html", graphJSON=graphJSON,
                           ccc_msg=ccc_msg, ccc_fatiguecheck=ccc_fatiguecheck,
                           ccc_pemcheck=ccc_pemcheck, ccc_paincheck=ccc_paincheck, ccc_sleepcheck=ccc_sleepcheck,
                           ccc_cogcheck=ccc_cogcheck, ccc_autocheck=ccc_autocheck, ccc_immunecheck=ccc_immunecheck,
                           ccc_neurocheck=ccc_neurocheck, ccc_dx=ccc_dx, ccc_reduction=ccc_reduction,
                           iomfatiguecheck=iomfatiguecheck, iomreductioncheck=iomreductioncheck,
                           iompemcheck=iompemcheck, iomdxcheck=iomdxcheck, iom_msg=iom_msg,
                           iomsleepcheck=iomsleepcheck, iomcogcheck=iomcogcheck)