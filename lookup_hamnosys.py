import os
import pandas as pd
from numpy import genfromtxt
import numpy as np
import sys
from constant import ham_lookup_dict, gloss_to_unicode
def get_hamnosys(df, gloss_input):

    hamnosys_list = []
    glosses = gloss_input.lower()
    glosses = glosses.replace('the', '')
    glosses = glosses.replace('is', '')
    gloss_list = glosses.split()
    for gloss in gloss_list:
        curr_gloss = gloss
        curr_gloss = curr_gloss.replace('.', '')
        curr_gloss = curr_gloss.replace(',', '')
        curr_gloss = curr_gloss.replace('!', '')
        df_lookup =df[df['gloss'].str.fullmatch(curr_gloss)]
        if len(df_lookup) == 0:
            hamnosys_list.append(str(""))  
        else:  
            hamnosys_list.append(str(df_lookup['hamnosys'].values[0]))
    
    return hamnosys_list


def hamnosys_lookup(input_gloss = None):
    
    # declare after argument init
    gloss2hamfile = './gloss_to_hamnosys.xlsx'
    G2H_df = pd.read_excel(gloss2hamfile)

    # should be language model output
    glosses = input_gloss if input_gloss else 'hello we the india'
    # use this hamnosys_list for your data input
    hamnosys_list = get_hamnosys(G2H_df, glosses)
    
    return hamnosys_list
    
def hamnosys_2_usc(hamnosys_list = None):
    
    hamnosys2usc_file = './hamnosys_text_2_ucs.csv'
    df = pd.read_csv(hamnosys2usc_file, skipinitialspace = True)
    df['hamnosys'] = df['hamnosys'].str.replace(" ", "")
    df['ucs'] = df['ucs'].str.replace(" ", "")
    
    ucs_list = []
    for hamword_list in hamnosys_list:
        ham_list = hamword_list.split(',')
        ucs_sublist = []
        for ham in ham_list:
          
          if ham in ham_lookup_dict.keys():
              ucs_value = ham_lookup_dict[ham]
              
          
          ucs_sublist.append(ucs_value)

        ucs_list.append("".join(ucs_sublist))
    return ucs_list
    

def gloss_unicode(gloss = None):
    uni_list = []
    gloss_list = gloss.lower().split(" ")
    for gloss in gloss_list:
        gloss = gloss.replace(' ', '')
        if gloss in gloss_to_unicode.keys():
            uni_list.append(gloss_to_unicode[gloss])
    return uni_list

if __name__ == '__main__':
  
  gloss_unicode("INDIAN SIGN LANGUAGE NEW WELCOME")
  # hamnosys_list = hamnosys_lookup()
  # ucs_list = hamnosys_2_usc(hamnosys_list)

