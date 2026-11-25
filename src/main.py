from pathlib import Path
import csv, math, itertools, time, json
import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/'data'/name).open(encoding='utf-8') as f: return list(csv.DictReader(f))
def load():
    g=nx.DiGraph()
    for r in read('nos.csv'): g.add_node(r['id'],pos=(float(r['x']),float(r['y'])))
    for r in read('ruas.csv'):
        g.add_edge(r['origem'],r['destino'],km=float(r['km']),min=float(r['min']))
    return g

def astar(g,a,b):
    return nx.astar_path(g,a,b,heuristic=lambda u,v:math.dist(g.nodes[u]['pos'],g.nodes[v]['pos']),weight='min')
def cost(g,path,key='min'): return sum(g[u][v][key] for u,v in zip(path,path[1:]))
def plan(g,orders,method):
    pending=list(orders); current='D'; seq=['D']; path=['D']; arrivals=[]; elapsed=0
    while pending:
        target=pending[0] if method=='manual' else min(pending,key=lambda v:(cost(g,astar(g,current,v)),v))
        leg=astar(g,current,target); elapsed+=cost(g,leg)+3; arrivals.append(elapsed); path.extend(leg[1:]); seq.append(target); pending.remove(target); current=target
    path.extend(astar(g,current,'D')[1:]); seq.append('D')
    return dict(seq=seq,path=path,km=cost(g,path,'km'),min=cost(g,path)+3*len(orders),arrivals=arrivals)
def main():
    g=load(); orders=[r['no'] for r in read('pedidos.csv')]; pos=nx.get_node_attributes(g,'pos')
    # Mesmos dois entregadores; referência manual usa ordem de chegada alternada.
    manual=[orders[::2],orders[1::2]]
    labels=KMeans(n_clusters=2,random_state=42,n_init=10).fit_predict([pos[n] for n in orders]); groups=[[n for n,l in zip(orders,labels) if l==i] for i in range(2)]
    out=ROOT/'outputs'; out.mkdir(exist_ok=True)
    scenarios={'Manual': [plan(g,z,'manual') for z in manual], 'A* + vizinho': [plan(g,z,'auto') for z in manual], 'K-Means + A*': [plan(g,z,'auto') for z in groups]}
    rows=[]
    for name,routes in scenarios.items():
        rows.append(dict(cenario=name,km=round(sum(r['km'] for r in routes),2),min_total=round(sum(r['min'] for r in routes),2),min_conclusao=round(max(r['min'] for r in routes),2),atrasos=sum(t>35 for r in routes for t in r['arrivals']),custo=round(sum(r['km'] for r in routes)*0.22,2)))
        assert sorted(n for r in routes for n in r['seq'][1:-1])==sorted(orders)
    with (out/'metricas.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    (out/'rotas.json').write_text(json.dumps(scenarios,indent=2,ensure_ascii=False),encoding='utf-8')
    # Validação de A* contra Dijkstra em todos os pares.
    for a,b in itertools.product(g.nodes,repeat=2): assert math.isclose(cost(g,astar(g,a,b)),nx.shortest_path_length(g,a,b,weight='min'))
    # BFS minimiza saltos, não tempo; DFS é demonstrativo.
    a,b='D','J'; bfs=nx.shortest_path(g,a,b); dfs=nx.shortest_path(nx.dfs_tree(g,a),a,b); comparison={k:{'path':p,'min':cost(g,p)} for k,p in [('BFS',bfs),('DFS',dfs),('A*',astar(g,a,b))]}
    (out/'buscas.json').write_text(json.dumps(comparison,indent=2),encoding='utf-8')
    fig,ax=plt.subplots(figsize=(8,5)); nx.draw_networkx(g,pos,ax=ax,node_color=['#e6a23c' if n=='D' else '#c9def0' for n in g],node_size=650,arrows=True,font_size=10); ax.set_title('Grafo viário fictício • D = restaurante'); ax.axis('off'); fig.tight_layout(); fig.savefig(out/'grafo.png',dpi=170); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5)); nx.draw_networkx_edges(g,pos,ax=ax,alpha=.18,arrows=False); nx.draw_networkx_nodes(g,pos,nodelist=['D'],node_color='#e6a23c',node_shape='s',ax=ax,node_size=700)
    for i,z in enumerate(groups): nx.draw_networkx_nodes(g,pos,nodelist=z,node_color=['#377eb8','#e67e22'][i],ax=ax,node_size=650,label=f'Zona {i+1}');
    nx.draw_networkx_labels(g,pos,ax=ax); ax.legend(); ax.set_title('Agrupamento espacial por K-Means'); ax.axis('off'); fig.tight_layout(); fig.savefig(out/'clusters.png',dpi=170); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4)); bars=ax.bar([r['cenario'] for r in rows],[r['min_conclusao'] for r in rows],color=['#8c939c','#4679a8','#237a57']); ax.bar_label(bars,fmt='%.1f'); ax.set_ylabel('Minutos'); ax.set_title('Tempo para concluir as entregas e retornar'); ax.set_ylim(0,max(r['min_conclusao'] for r in rows)*1.2); fig.tight_layout(); fig.savefig(out/'comparacao.png',dpi=170); plt.close(fig)
    print(json.dumps(rows,ensure_ascii=False,indent=2)); print('Validação A* x Dijkstra: OK'); print(comparison)
if __name__=='__main__': main()
