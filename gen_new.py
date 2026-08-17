# -*- coding: utf-8 -*-
# Yeni cevaplar listesinden 5x5 Baklava bulmacalari uret
from wordfreq import zipf_frequency
from collections import defaultdict
import json

UP={'a':'A','b':'B','c':'C','ç':'Ç','d':'D','e':'E','f':'F','g':'G','ğ':'Ğ','h':'H',
    'ı':'I','i':'İ','j':'J','k':'K','l':'L','m':'M','n':'N','o':'O','ö':'Ö','p':'P',
    'r':'R','s':'S','ş':'Ş','t':'T','u':'U','ü':'Ü','v':'V','y':'Y','z':'Z'}
def up(w): return ''.join(UP[c] for c in w)

low=[l.strip() for l in open('/home/user/trpuzzle4/kelimehavuzu.txt',encoding='utf-8') if l.strip()]
pairs=[(up(w),w) for w in low if len(w)==5]
pairs.sort(key=lambda p:-zipf_frequency(p[1],'tr'))
words=[W for W,_ in pairs]
freq={W:zipf_frequency(w,'tr') for W,w in pairs}
rank={W:i for i,W in enumerate(words)}
POOL=set(words)
print("havuz:",len(words))
print("en yaygin 25:"," ".join(words[:25]))

# Bulmaca cevabi olarak uygun olmayan birkac kelime (havuzda kalir, cevap olarak secilmez)
AVOID=set("""ZENCİ GAVUR DÜRZÜ IRKÇI FUHUŞ CÜNÜP AYYAŞ AHRAZ ALLAH HAÇLI ŞAFİİ SÜNNİ MÜMİN
KAFİR MELUN ZALİM AHMAK APTAL SALAK MORUK HERİF RÜKÜŞ ŞIPAR ŞOPAR LAVUK GEBEŞ DENYO
BÜCÜR HÖDÜK PAÇOZ YOSMA ZÜPPE ZORBA VULVA SİDİK KABIZ İSHAL HADIM SEKSİ""".split())

downmap=defaultdict(lambda: defaultdict(list))
for w in words:
    downmap[(w[0],w[2])][w[4]].append(w)
def best_down(cs): return min(cs,key=lambda w:rank[w])

# yaygin ve uygun kelimeler oncelikli
common=[W for W in words if freq[W]>=2.6 and W not in AVOID]
print("aday cekirdek (zipf>=2.6):",len(common))

cands=[]; seen=set(); per_a0=defaultdict(int)
for a0 in common:
    if per_a0[a0]>=10: continue
    got=0
    for a1 in common:
        s0=downmap.get((a0[0],a1[0])); s1=downmap.get((a0[2],a1[2])); s2=downmap.get((a0[4],a1[4]))
        if not(s0 and s1 and s2): continue
        for a2 in common:
            if a2[0] in s0 and a2[2] in s1 and a2[4] in s2:
                d0=best_down(s0[a2[0]]); d1=best_down(s1[a2[2]]); d2=best_down(s2[a2[4]])
                allw={a0,a1,a2,d0,d1,d2}
                if len(allw)!=6: continue
                if any(w in AVOID for w in allw): continue
                key=tuple(sorted(allw))
                if key in seen: continue
                seen.add(key)
                cands.append((sum(rank[w] for w in allw),[a0,a1,a2],[d0,d1,d2]))
                per_a0[a0]+=1; got+=1
                break
        if got>=10: break
    if len(cands)>=20000: break

cands.sort(key=lambda x:x[0])
print("aday bulmaca:",len(cands))

selected=[]; used=defaultdict(int); pf=defaultdict(int)
for score,ac,dn in cands:
    ws=ac+dn
    if pf[ac[0]]>=4: continue
    if any(used[w]>=6 for w in ws): continue
    selected.append({"across":ac,"down":dn})
    pf[ac[0]]+=1
    for w in ws: used[w]+=1
    if len(selected)>=260: break

# dogrula
for p in selected:
    a=p["across"]; d=p["down"]
    assert a[0][0]==d[0][0] and a[1][0]==d[0][2] and a[2][0]==d[0][4]
    assert a[0][2]==d[1][0] and a[1][2]==d[1][2] and a[2][2]==d[1][4]
    assert a[0][4]==d[2][0] and a[1][4]==d[2][2] and a[2][4]==d[2][4]
    for w in a+d: assert w in POOL, "havuz disi: "+w
    assert len(set(a+d))==6

json.dump(selected,open('/tmp/claude-0/-home-user-trpuzzle4/3c82a689-4f63-5aef-afcd-444c23ed6558/scratchpad/puzzles_new.json','w'),ensure_ascii=False)
print("SECILEN:",len(selected))
for i,p in enumerate(selected[:12]):
    print(f"[{i:2}] {' '.join(p['across'])} | {' '.join(p['down'])}")
