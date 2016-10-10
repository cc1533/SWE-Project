import os
from subprocess import call

#import subprocess

os.environ['MALLET_HOME'] = "C:\\mallet"


# This script assumes it will be run from inside C:\mallet-2.0.7

# Set the path to your mallet package (make sure to change the mallet version number, if necessary)
# Create directory "inputdirectory" within this mallet directory. Load the files to be analyzed in "inputdirectory"
mallet_path = "C:\\mallet"
input_path = mallet_path + "\\inputdirectory"

# Specify the number of topics you wish to obtain, and tbe number of iterations you wish to use
# to obtain those topics. Store both values as string (keep the numbers in quotation marks, or use str() method below)
# Caveat lector: Running 30000 iterations takes a few minutes...
num_topics = "10"
num_iterations = "20"

# One could add additional parameters here (e.g. --optimize-interval could be helpful)

class Mallet(object):
    def __init__(self, input_path, mallet_path):
        self.mallet_exec = mallet_path + "\\bin\\mallet"
        self.input_path = mallet_path + "\\inputdirectory"
    
    def import_dir(self):
        text_path = self.input_path 
        output = "readyforinput.mallet"
        call(self.mallet_exec + " import-dir --input " + input_path + " --keep-sequence --output " + output , shell=True)
    
    def train_topics(self):
        input_file = mallet_path + "\\readyforinput.mallet"
        output_dir = mallet_path + "\\topic_modelling_output\\"
        output_doc_topics = output_dir + "\\output_doc_topics.txt"
        output_topic_keys = output_dir + "\\output_topic_keys.txt"
        output_state = output_dir + "\\output_state.gz"
        command = self.mallet_exec + " train-topics --input " + input_file + " --num-topics " + num_topics + " --output-doc-topics " + output_doc_topics + " --output-topic-keys " + output_topic_keys + " --output-state " + output_state + " --num-iterations " + num_iterations
        call(command, shell=True)

callmallet = Mallet(input_path, mallet_path)
callmallet.import_dir()
callmallet.train_topics()

# how to hardcode path: os.path.abspath("mydir\\myfile.txt")
