import pandas as pd
import numpy as np

# DSQ items grouped according to CCC domains and scoring syntax @ https://www.leonardjason.com/cfsme_measures-2/
fatigue_domain = ['fatigue13f', 'fatigue13s']

pem_domain = ['heavy14f', 'soreness15f', 'mental16f', 'minimum17f', 'drained18f',
              'heavy14s', 'soreness15s', 'mental16s', 'minimum17s', 'drained18s']

sleep_domain = ['unrefreshed19f', 'nap20f', 'falling21f', 'staying22f', 'early23f', 'allday24f',
                'unrefreshed19s', 'nap20s', 'falling21s', 'staying22s', 'early23s', 'allday24s']

pain_domain = ['musclepain25f', 'jointpain26f', 'eyepain27f', 'chestpain28f', 'bloating29f', 'stomach30f', 'headaches31f',
               'musclepain25s', 'jointpain26s', 'eyepain27s', 'chestpain28s', 'bloating29s', 'stomach30s', 'headaches31s']

cog_domain = ['twitches32f', 'weakness33f', 'noise34f', 'lights35f', 'remember36f', 'difficulty37f', 'word38f', 'understanding39f', 'focus40f', 'unable41f', 'depth42f', 'slowness43f', 'absent44f',
              'twitches32s', 'weakness33s', 'noise34s', 'lights35s', 'remember36s', 'difficulty37s', 'word38s', 'understanding39s', 'focus40s', 'unable41s', 'depth42s', 'slowness43s', 'absent44s']

autonomic_domain = ['bladder45f', 'bowel46f', 'nausea47f', 'unsteady48f', 'shortness49f', 'dizz50f', 'irregular51f', 
                    'bladder45s', 'bowel46s', 'nausea47s', 'unsteady48s', 'shortness49s', 'dizz50s', 'irregular51s']

neuro_domain = ['weight52f', 'appetite53f', 'sweating54f', 'night55f', 'limbs56f', 'chills57f', 'hot58f', 'htemp59f', 'ltemp60f', 'alcohol61f', 
                'weight52s', 'appetite53s', 'sweating54s', 'night55s', 'limbs56s', 'chills57s', 'hot58s', 'htemp59s', 'ltemp60s', 'alcohol61s']

immune_domain = ['sorethroat62f', 'lymphnodes63f', 'fever64f', 'flu65f', 'smells66f', 
                'sorethroat62s', 'lymphnodes63s', 'fever64s', 'flu65s', 'smells66s']

# domains for the short form:
sf_fatigue_domain = ['fatigue13f', 'fatigue13s']
sf_pem_domain = ['soreness15f', 'soreness15s', 'minimum17f', 'minimum17s']
sf_sleep_domain = ['unrefreshed19f', 'unrefreshed19s']
sf_pain_domain = ['musclepain25f', 'musclepain25s', 'bloating29f', 'bloating29s']
sf_cog_domain = ['remember36f', 'remember36s', 'difficulty37f', 'difficulty37s']
sf_autonomic_domain = ['bowel46f', 'bowel46s', 'unsteady48f', 'unsteady48s']
sf_neuro_domain = ['limbs56f', 'limbs56s', 'hot58f', 'hot58s']
sf_immune_domain = ['flu65f', 'flu65s', 'smells66f', 'smells66s']

#Maybe change this to the imputed data:
df = pd.read_csv('utils/MECFS and Controls F+S Reduction.csv')
sdf = pd.read_csv('utils/MECFS and Controls F+S Reduction.csv')

df['fatigue_mean'] = np.mean(df[fatigue_domain], axis=1)
df['pem_mean'] = np.mean(df[pem_domain], axis=1)
df['sleep_mean'] = np.mean(df[sleep_domain], axis=1)
df['pain_mean'] = np.mean(df[pain_domain], axis=1)
df['cog_mean'] = np.mean(df[cog_domain], axis=1)
df['auto_mean'] = np.mean(df[autonomic_domain], axis=1)
df['neuro_mean'] = np.mean(df[neuro_domain], axis=1)
df['immune_mean'] = np.mean(df[immune_domain], axis=1)

sdf['fatigue_mean'] = np.mean(sdf[sf_fatigue_domain], axis=1)
sdf['pem_mean'] = np.mean(sdf[sf_pem_domain], axis=1)
sdf['sleep_mean'] = np.mean(sdf[sf_sleep_domain], axis=1)
sdf['pain_mean'] = np.mean(sdf[sf_pain_domain], axis=1)
sdf['cog_mean'] = np.mean(sdf[sf_cog_domain], axis=1)
sdf['auto_mean'] = np.mean(sdf[sf_autonomic_domain], axis=1)
sdf['neuro_mean'] = np.mean(sdf[sf_neuro_domain], axis=1)
sdf['immune_mean'] = np.mean(sdf[sf_immune_domain], axis=1)
