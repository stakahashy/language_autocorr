# language_autocorr
A python implementation of "Long-Range Memory in Literary Texts: On the Universal Clustering of the Rare Words"(2016) authored by Kumiko Tanaka-Ishii and Armin Bunde. It works on python2.7 and python3.6 environment (the results may slightly differ). 

# Usage
1. Install the dependencies by "pip install -r requirements.txt".
2. Run the script by "python auto_correlation.py file_name.txt".
This script generates file_name_language_acf.png, the double log plot of the auto-correlation function of the text.

# Notes
## Text format
In our implementation, the split symbol between words in the text file is expect to be '\n'. 
We put mobyDick.txt as an example retrieved from Gutenberg project. The text file is preprocessed to exclude irrelevant texts to the content.
You can simply modify it by updating "splitter = '\n'" in line 40.

## Parameter
The parameter of this quantification methodology is Q which defines the ratio of rare words (1/Q) in a text.
It is set to 16 as default in line 34. 
