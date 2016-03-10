
import re
#(ROOT (S (NP (DT A) (NN record) (NN date)) (VP (VBZ has) (RB n't) (VP (VBN been) (VP (VBN set)))) (. .)))

sentence = ['NP', ['DT', 'A'], ['NN', 'record'], ['NN','date']]
#[NP, [DT, A],[@NP->DT, [NN, record],[ '@NP->_DT_NN' , ['NN' , 'date']]]]

#for element in sentence:
#	if isinstance(element, list) and element[0].isupper():




def binarize(sentence):
	Path = "@" + sentence[0] + "->_"
	branches = sentence[1:]
	branchLength = len(branches)
	branches = [branches[i][0] for i in range(branchLength)]
	
	if(not sentence[0].isalpha() or not isinstance(sentence[1],list)):
		return sentence
	if(branchLength == 2):
		return [sentence[0], binarize(sentence[1]) ,binarize(sentence[1])]
	if(branchLength == 1):
		return [sentence[0], binarize(sentence[1])]

	def b(Path ,i):
		currentLoc = branches[i-2]
		if( i == branchLength):
			newPath = Path + '_' + currentLoc 
			return [newPath , sentence[i]]
		else:
			i += 1
			newPath = Path + '_' + currentLoc 
			return [ newPath, sentence[i-1]] + [b(newPath,i)]
			
	return sentence[:2]+[b(Path,2)]



print(binarize(sentence))


