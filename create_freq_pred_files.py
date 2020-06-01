import numpy as np
import pickle
import codecs
#import chardet
from read_saccade_data import get_words, get_pred

# Detect text encoding
# rawdata=open("texts/frequency_german.txt","r").read()
# print chardet.detect(rawdata)

#to prevent unicode errors
# 'utf-8' 'cp1252' 'ISO-8859-1'
# with codecs.open("frequency_german.txt", 'r', encoding = 'ISO-8859-1',errors = 'strict') as mytext:

## Converter function to use
comma_to_dot = lambda s: float(s.replace(",","."))
decode_uft8 = lambda x: x.decode("utf-8", errors="strict")
decode_ISO= lambda x: x.decode('ISO-8859-1', errors="strict")
encode_uft8 = lambda x: x.encode("utf-8",errors="strict")
#replace_german = lambda x: unidecode(x)
to_lowercase = lambda x: x.lower()

## Set converters
convert_dict = {0:decode_ISO,4:comma_to_dot, 5:comma_to_dot, 9:comma_to_dot}
#{column:comma_to_dot for column in [4,5,9]}

## Get selected columns from text
freqlist_arrays = np.genfromtxt("Texts/frequency_german.txt", dtype=[('Word','U30'),('FreqCount','i4'), ('CUMfreqcount','i4'),('Subtlex','f4'), ('lgSubtlex','f4'), ('lgGoogle','f4')],
                                    usecols = (0,1,3,4,5,9), converters= convert_dict , skip_header=1, delimiter="\t")

freqthreshold = 1.5
nr_highfreqwords = 200

def create_freq_file(freqlist_arrays, freqthreshold, nr_highfreqwords):
    ## Sort arrays ascending on subtlex by million
    freqlist_arrays = np.sort(freqlist_arrays,order='lgSubtlex')[::-1]
    select_by_freq = np.sum(freqlist_arrays['lgSubtlex']>freqthreshold)
    freqlist_arrays = freqlist_arrays[0:select_by_freq]

    ## Clean and select frequency words and frequency
    freq_words = freqlist_arrays[['Word','lgSubtlex']]
    frequency_words_np = np.empty([len(freq_words),1],dtype='U20')
    frequency_words_dict  = {}
    for i,line in enumerate(freq_words):
        frequency_words_dict[line[0].replace(".","").lower()] = line[1]
        frequency_words_np[i] = line[0].replace(".","").lower()

    cleaned_psc_words = get_words()
    overlapping_words = np.intersect1d(cleaned_psc_words,frequency_words_np, assume_unique=False)

    ## IMPORTANT TO USE unicode() to place in dictionary, to replace NUMPY.UNICODE!!
    ## Match PSC and freq words and put in dictionary with freq
    file_freq_dict = {}
    for i,word in enumerate(overlapping_words):
        file_freq_dict[unicode(word.lower())] = frequency_words_dict[word]

    ## Put top freq words in dict, can use np.shape(array)[0]):
    for line_number in xrange(nr_highfreqwords):
        file_freq_dict[unicode((freq_words[line_number][0]).lower())] = freq_words[line_number][1]

    output_file_frequency_map = "Data\PSCall_frequency_map.dat"
    with open (output_file_frequency_map,"w") as f:
        pickle.dump(file_freq_dict,f)


def create_pred_file():
    file_pred_dict = get_pred()

    output_file_predictions_map = "Data\PSCall_predictions_map.dat"
    with open (output_file_predictions_map,"w") as f:
	    pickle.dump(file_pred_dict,f)

create_freq_file(freqlist_arrays,freqthreshold,nr_highfreqwords)
create_pred_file()