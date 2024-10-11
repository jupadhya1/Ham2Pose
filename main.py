import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from GPT.generate import GPT_main
from Ham2Pose.test import main
from Ham2Pose.args import args
from Pose2Mesh.demo.run import mesh_fit
from lookup_hamnosys import hamnosys_lookup, hamnosys_2_usc, gloss_unicode
import numpy as np
import sys
if __name__ == '__main__':
    
    '''
    Text to Gloss from Veblen-main
    There is some issue with the checkpoint
    ''' 
    '''
    Hello everyone from Expression-AI.
    Deaf people in India face communication barriers. 
    If all information is in ISL, deaf people will understand, barriers would be minimized, communication breakdowns will be fixed and communication will be smooth.
    We at expression.AI make communication easy by providing ISL translation of information on the internet, anytime and from anywhere.
    If you have doubts, or questions, we can answer them. 
    Have a good day!
    '''
    # sentence = "welcome to news in indian sign language!"
    sentence = "Have a good day!"
    gloss = GPT_main(sentence)
    print(gloss)
    
    # gloss = 'indian sign language new welcome'
    # gloss = 'welcome'

    '''
    Gloss to Hamnosystext from Hamnosyslookup
    ''' 

    # hamnosys_text = hamnosys_lookup(gloss)
    # ucs_list = hamnosys_2_usc(hamnosys_text)
    ucs_list = gloss_unicode(gloss)
    
    # ucs_list = "".join(ucs_list)    
    
    # print(f"len of the gloss = {len(ucs_list)}")

    '''
    Calling Ham2Pose main function - getting a list of Keypoints for each word
    input - from the Ham2Pose/data and args  
    '''
    output_kps = main(args, text_list= ucs_list)
    
    # Sanity check to see if it works with a saved kp
    # kp = np.load("./Ham2Pose/output_pose/full/3258.npy")

    print(f"len of the keypoints list = {len(output_kps)}")
    
    '''
    Sample mesh fitting for each sequence of Keypoints
    
    '''
    for i in range(len(output_kps)):
        print(f"gloss_{i} processed")
        mesh_fit(output_kps[i], f"gloss_{i}")
    
    
    combined_kp = None
    k = 0.2 # percentage of cut
    for i in range(len(output_kps)):
        frames = output_kps[i].shape[0]
        print(f"count = {int(0.6  * frames)}")
        if i == 0:
            combined_kp = output_kps[i][: - int(k*frames)]
        elif i == len(output_kps) - 1:
            combined_kp = np.concatenate((combined_kp, output_kps[i][int(k*frames) : ]), axis= 0) 
        else:
            combined_kp = np.concatenate((combined_kp, output_kps[i][int(k*frames) : - int(k*frames)]), axis= 0)
    
    # print(combined_kp.shape)
    mesh_fit(combined_kp, "new_2_full_0.2")
    
    