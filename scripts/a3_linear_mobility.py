"""A3: 粒子ロス L=sqrt(g) a^k を ρ' = -K_ρ(Q/k) と書く線形移動度 Onsager 作用素の検算。
K_ρ(X) = -(g/2)([L0,ρ[X,L0†]] + [[L0,X]ρ,L0†]),  L0=a^k,  Q=N (切断した数演算子)。"""
import numpy as np, scipy.linalg as la
rng=np.random.default_rng(1)
def rand_rho(d):
    A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); r=A@A.conj().T; return r/np.trace(r)
def com(A,B): return A@B-B@A
def setup(M,k):
    d=M+1; a=np.diag(np.sqrt(np.arange(1,d)),1).astype(complex); N=np.diag(np.arange(d)).astype(complex)
    return d,a,N,np.linalg.matrix_power(a,k)
def Kop(rho,X,L0,g):
    return -(g/2)*(com(L0,rho@com(X,L0.conj().T))+com(com(L0,X)@rho,L0.conj().T))
def lind(rho,L0,g): return g*(L0@rho@L0.conj().T-0.5*(L0.conj().T@L0@rho+rho@L0.conj().T@L0))
for M,k in [(6,1),(8,2),(9,3)]:
    d,a,N,L0=setup(M,k); g=0.7
    print("M,k",M,k,"[N,a^k]+k a^k =",np.abs(com(N,L0)+k*L0).max())
    rho=rand_rho(d)
    # 恒等式 rho' = -K(N/k)
    print("  |rho'+K(N/k)| =",np.abs(lind(rho,L0,g)+Kop(rho,N/k,L0,g)).max())
    # K のエルミート性・対称性・半正定値性（実エルミート空間上の行列表示）
    basis=[]
    for i in range(d):
        for j in range(i,d):
            E=np.zeros((d,d),complex)
            if i==j: E[i,i]=1
            else: E[i,j]=E[j,i]=1; basis.append(E.copy()); E=np.zeros((d,d),complex); E[i,j]=1j; E[j,i]=-1j
            basis.append(E)
    n=len(basis); G=np.zeros((n,n))
    for p in range(n):
        for q in range(n): G[p,q]=np.trace(basis[p]@Kop(rho,basis[q],L0,g)).real
    ev=np.linalg.eigvalsh((G+G.T)/2)
    print("  asym",np.abs(G-G.T).max(),"min eig",ev.min(),"#zero",(abs(ev)<1e-10).sum())
    # ハミルトニアン H=f(N) 共存: 電荷 Q は H の下で保存、E = Tr(rho N)/k の変化率
    H=np.diag(rng.normal(size=d)).astype(complex)
    drho=-1j*com(H,rho)+lind(rho,L0,g)
    print("  dE/dt =",np.trace(N@drho).real/k," vs -g Tr(rho L0†L0)/... =",-g*np.trace(rho@L0.conj().T@L0).real)
# 熱的ゲイン付き（古典・対角部分）で q→0 の極限: log(1/q) 倍した辺の伝導度 -> (n+1) p_{n+1}
def LM(x,y): return x if abs(x-y)<1e-14 else (x-y)/(np.log(x)-np.log(y))
p=rng.random(6); p/=p.sum()
for q in [1e-2,1e-4,1e-8,1e-16]:
    kap=[LM(p[n+1]/q**(n+1),p[n]/q**n)*q**(n+1)*(n+1)/(1-q) for n in range(5)]
    print(q,np.array(kap)*np.log(1/q)/np.array([(n+1)*p[n+1] for n in range(5)]))
