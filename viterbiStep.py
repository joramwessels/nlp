import numpy as np
import pandas as pd
"""
Viterbi step on the example data from Speech and Language processing ch 5 p25
"""
Index = ['VB','TO','NN','PPSS']
#transRowIndex = ['<s>','VB','TO','NN','PPSS']
sTransProbs = np.array([.019,.0043,.041,.067])
transProbs = np.array([[.0038,.035,.047,.0070],[.83,.0,.00047,.0],[.0040,.016,.087,.0045],[.23,.00079,.0012,.00014]])
observProbs = np.array([[.0,.0093,.0,.00012],[.0,.0,.99,.0],[.0,.000054,.0,.00057],[.37,.0,.0,.0]])
tagSeq= []
HighestValue = 0

N = observProbs.shape[0] #amount of tags
T = observProbs.shape[1] #amount of word observations
viterbi = np.zeros((N,T))

viterbi[:,0] = sTransProbs*observProbs[:,0]
tagSeq.append(Index[np.argmax(viterbi[:,0])]) # adds tag with the highest probability

for t in range(1,T):
	for s in range(0,N):
		viterbi[s,t] = np.max(viterbi[:,t-1]*transProbs[:,s])*observProbs[s,t]
	tagSeq.append(Index[np.argmax(viterbi[:,t])])	
	
print(viterbi)
print(tagSeq)

	
#correct sequence ppss vb to vb