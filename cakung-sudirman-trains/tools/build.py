import json
d=json.load(open('parsed.json'))
B={r['no']:r for r in d['B']}
def m(t):
    h,mm=map(int,t.split(':')); v=h*60+mm
    return v+1440 if h<3 else v
trips={"CUK_SUD":[], "SUD_CUK":[]}
for r in d['A']:
    t=r['t']
    if 'CUK' in t and 'SUD' in t:
        trips['CUK_SUD'].append(dict(no=r['no'],rel=r['rel'],dep=t['CUK'],arr=t['SUD'],via='direct',dest=r['rel'].split(' - ')[0].split('-')[-1]))
    elif 'CUK' in t and r['no2'] and r['no2'] in B and 'SUD' in B[r['no2']]['t']:
        b=B[r['no2']]
        trips['CUK_SUD'].append(dict(no=r['no']+'/'+r['no2'],rel=r['rel'],dep=t['CUK'],arr=b['t']['SUD'],via='kpb',kpb=t['KPB'],dest=b['rel'].split('-')[-1]))
    if 'SUD' in t and r['no2'] and r['no2'] in B and 'CUK' in B[r['no2']]['t'] and 'CUK' not in t or ('SUD' in t and r['no2'] and r['no2'] in B and 'CUK' in B[r['no2']]['t']):
        b=B[r['no2']]
        trips['SUD_CUK'].append(dict(no=r['no']+'/'+r['no2'],rel=r['rel'],dep=t['SUD'],arr=b['t']['CUK'],via='kpb',kpb=t['KPB'],dest=b['rel'].split('-')[-1]))
for r in d['B']:
    t=r['t']
    if 'SUD' in t and 'CUK' in t:
        trips['SUD_CUK'].append(dict(no=r['no'],rel=r['rel'],dep=t['SUD'],arr=t['CUK'],via='direct',dest=r['rel'].split('-')[-1]))
for k,v in trips.items():
    v.sort(key=lambda x:m(x['dep']))
    for x in v: x['dur']=m(x['arr'])-m(x['dep'])
    import collections
    print(k,len(v),collections.Counter(x['via'] for x in v), 'dur range', {via:(min(x['dur'] for x in v if x['via']==via),max(x['dur'] for x in v if x['via']==via)) for via in ('direct','kpb')})
json.dump(trips,open('trips.json','w'))
out={k:[[x['dep'],x['arr'],x['no'],1 if x['via']=='kpb' else 0,x['rel'],x.get('kpb','')] for x in v] for k,v in trips.items()}
open('data.js','w').write('const DATA='+json.dumps(out,separators=(',',':'))+';')
