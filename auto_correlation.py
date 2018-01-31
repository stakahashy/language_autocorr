import operator
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Author of this program: Shuntaro Takahashi and Kumiko Tanaka-Ishii

# This program is an implementation of "Long-Range Memory in 
# Literary Texts: On the Universal Clustering of the Rare Words"
# authored by: Kumiko Tanaka-Ishii and Armin Bunde                                     
# URL: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0164658
# This method is used in the following paper as well:
# "Do neural nets learn statistical laws behind natural language?"
# http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0189326
# authored by: Shuntaro Takahashi and Kumiko Tanaka-Ishii

def auto_correlation(x,lag = 1):
    a = pd.Series(np.reshape(x,(-1)))
    b = a.autocorr(lag = lag)
    if np.isnan(b) or np.isinf(b):
        return 0
    return b

#check the args
assert len(sys.argv) == 2, "No input file name or too many args" 

#file 
file_name = sys.argv[1]

#setting parameters
q = 16. # The parameter Q in the original paper
ratio = 1/q  # the ratio of least frequent words among all words are defined as the set of "rare words"
             # NOTE: ratio is NOT among the vocabulary of text
             
max_lag_fraction = 100 #the lag for acf calculation is up to the 1% of the length of sequence

splitter = '\n' #the split symbol between words in the input file

#load_file
with open(file_name,'r') as r:
    s = r.read()
words = s.split(splitter)

#construct vocabulary : count the frequency of each word in order to extract rare words of the text
vocabulary = dict()
for word in words:
    if word in vocabulary:
        vocabulary[word] += 1
    else:
        vocabulary[word] = 1                                          
print('The constructed vocabulary size is %i'%(len(vocabulary)))

#extract rare words from the vocabulary from the vocabulary
sorted_vocabulary = sorted(vocabulary.items(), key=operator.itemgetter(1))
max_count = int(ratio*len(words))
count = 0
rare_words = []
for e in sorted_vocabulary:
    count += e[1]
    if count > max_count:
        break
    rare_words.append(e[0])
print('The number of rare word is %i'%(len(rare_words)))

#construct a time series whose elements are the index (offset, or location) of the rare words extracted
series = []
for i,word in enumerate(words):
    if i % 10000 == 0:
        print('%2.1f %% of text processed for series construction'%(100*(float(i)/len(words))))
    if word in rare_words:
        series.append(i)

#construct a time series of intervals of rare words by taking the difference of the series

series = np.diff(series)

#the maximum lag for auto-correlation computation is restricted up to 1% of the length of the series
max_lag = series.size//max_lag_fraction

#prepare log-bin lags
x = [i for i in range(1,11)]
c = 1.2
xt = int(x[-1]*c)
while xt < max_lag:
    x.append(xt)
    xt = int(x[-1]*c)
x.append(max_lag)

#compute auto-correlation
ac  = []
for i in x:
    ac.append(auto_correlation(series,i))
    if i != 0 and i%100 == 0:
        print('auto-correlation calculated up to lag = %i'%i)

#plot it in log-log scale
plt.figure()
plt.plot(x,ac,'.')
plt.xscale('log')
plt.yscale('log')
plt.ylim(0.001,1)
plt.xlabel('lag')
plt.ylabel('auto-correlation')
plt.savefig(file_name.split('.')[0]+'_language_acf.png')
