import pandas as pd
import pygsheets
import datetime

def build_dataframe_for_export (session):
  df = pd.DataFrame()
  df['sid'] = [session.sid]
  # stores UTC time timestamp
  df['date'] = datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y")
  df['time'] = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
  df['ip'] = session['ip']
  # add all items currently collected to the data frame
  for item in session:
    if item in dsq_columns:
      df[item] = [session[item]]
  return df

def dump_collected_data_to_sheet(df):
  gc = pygsheets.authorize(service_file='utils/dsqscreen-401016-0e6db07e3d56.json')
  sh = gc.open('DSQScreen Output')
  wks=sh[0]
  session_row = wks.find(df['sid'][0])
  if bool(session_row):
    wks.update_values(session_row[0].label, values=df.values.tolist())
  else:
    next_row = next_available_row(wks)
    wks.update_values("A" + next_row, df.values.tolist())

def next_available_row(wks):
    # returns a string of length of column 1 + 1
    return str(len(wks.get_col(1,include_tailing_empty=False)) + 1)

dsq_columns = ["fatiguescoref",
"fatiguescores",
"minexf",
"minexs",
"sleepf",
"sleeps",
"rememberf",
"remembers",
"soref",
"sores",
"attentionf",
"attentions",
"musclef",
"muscles",
"bloatf",
"bloats",
"bowelf",
"bowels",
"unsteadyf",
"unsteadys",
"limbsf",
"limbss",
"hotf",
"hots",
"fluf",
"flus",
"smellf",
"smells",
"reduction",
"viral",
"heavyf",
"heavys",
"mentalf",
"mentals",
"drainedf",
"draineds",
"napf",
"naps",
"fallf",
"falls",
"stayf",
"stays",
"earlyf",
"earlys",
"alldayf",
"alldays",
"jointpainf",
"jointpains",
"eyepainf",
"eyepains",
"chestpainf",
"chestpains",
"stomachf",
"stomachs",
"headachesf",
"headachess",
"twitchesf",
"twitchess",
"weakf",
"weaks",
"noisef",
"noises",
"lightsf",
"lightss",
"wordf",
"words",
"understandf",
"understands",
"focusf",
"focuss",
"visionf",
"visions",
"depthf",
"depths",
"slowf",
"slows",
"absentf",
"absents",
"bladderf",
"bladders",
"nauseaf",
"nauseas",
"shortf",
"shorts",
"dizzyf",
"dizzys",
"heartf",
"hearts",
"weightf",
"weights",
"appetitef",
"appetites",
"sweatf",
"sweats",
"nightf",
"nights",
"chillsf",
"chillss",
"hitempf",
"hitemps",
"lotempf",
"lotemps",
"alcoholf",
"alcohols",
"throatf",
"throats",
"lymphnodesf",
"lymphnodess",
"feverf",
"fevers",
"intolerant"]
