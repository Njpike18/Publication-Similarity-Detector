#
# Final Project Parts 1 and 2
# Pair Optional: Done in collaboration with Richard Quach, Quachr@bu.edu

import math

class TextModel:
    """Creates an object TextModel
    """
   
    def __init__(self,model_name):
        """Initializes the TextModel name, and creates dictionaries for the words
            And word lengths """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths= {}
        self.punctuation = {}
    
    
    def __repr__(self):
        """returns a string that includes the name of the model as well
        as the sizes of the dictionary for each feature of the text
        """
        s ='text model name: ' + self.name + '\n' 
        s+='number of words: ' + str(len(self.words)) + '\n' 
        s+='number of word lengths: ' + str(len(self.word_lengths)) +'\n'
        s+= 'number of stems: ' + str(len(self.stems)) + '\n'
        s+= 'number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s+= 'number of punctuations: ' + str(len(self.punctuation)) + '\n'
        return s


    def add_string(self,s):
        """Adds a string to the dictionaries of TextModel
        """
        p_s = s.split()
        if len(p_s) in self.sentence_lengths:
           self.sentence_lengths[len(p_s)] += 1
        else: 
           self.sentence_lengths[len(p_s)] = 1

        
                    
       
        
       
        for w in p_s:
            for ch in w:
                if ch in """.,?"'!;:""":
                    if ch in self.punctuation:
                        self.punctuation[ch] += 1
                    else:
                        self.punctuation[ch] = 1
        
        word_list = clean_text(s)
        for w in word_list:
            if w in self.words:
                self.words[w] +=1
            else:
                self.words[w] = 1
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1
            if stem(w) in self.stems:
                self.stems[stem(w)] += 1
            else:
                self.stems[stem(w)] =1
            
    
    def add_file(self,filename):
        """Similarly to add_string, adds a text file to the dictionaries
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        string = f.read()
        self.add_string(string)
        
    def save_model(self):
        """Saves the dictionaries of TextModel into separate files"""
        file_name = self.name + '_' + 'words'
        file_name2 = self.name + '_' + 'word_lengths'
        file_name3 = self.name + '_' + 'stems'
        file_name4 = self.name + '_' + 'sentence_lengths'
        file_name5 = self.name + '_' + 'punctuation'
        f = open(file_name, 'w')
        f.write(str(self.words))
        f.close()
        f2 = open(file_name2, 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        f3 = open(file_name3, 'w')
        f3.write(str(self.stems))
        f3.close
        f4 = open(file_name4, 'w')
        f4.write(str(self.sentence_lengths))
        f4.close
        f5 = open(file_name5, 'w')
        f5.write(str(self.punctuation))
        f5.close
        
        
    def read_model(self):
        """reads the dictionaries of a text file
        """
        file_name = self.name + '_' + 'words'
        file_name2 = self.name + '_' + 'word_lengths'
        file_name3 = self.name + '_' + 'stems'
        file_name4 = self.name + '_' + 'sentence_lengths'
        file_name5 = self.name + '_' + 'punctuation'
        f = open(file_name, 'r')
        f2 = open(file_name2, 'r')
        f3 = open(file_name3, 'r')
        f4 = open(file_name4, 'r')
        f5 = open(file_name5, 'r')

        d_str = f.read()
        d2_str = f2.read()           # Read in a string that represents a dict.
        d3_str = f3.read()
        d4_str = f4.read()
        d5_str = f5.read()
        f.close()

        self.words = dict(eval(d_str))      # Convert the string to a dictionary.
        self.word_lengths = dict(eval(d2_str))
        self.stems = dict(eval(d3_str))
        self.sentence_lengths = dict(eval(d4_str))
        self.punctuation = dict(eval(d5_str))
        
    def similarity_scores(self,other):
        """docstring"""
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score= compare_dictionaries(other.stems,self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation,self.punctuation)
        return [word_score, word_lengths_score, stems_score, sentence_lengths_score, punctuation_score]
    
    def classify(self, source1, source2):
        """docstring"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        s = ''
        s+= 'scores for ' + source1.name +': ' + str(scores1) + '\n'
        s+= 'scores for ' + source2.name + ': ' + str(scores2) + '\n'
        x = 0
        y = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                x+=1
            elif scores2[i] > scores1[i]:
                y+=1
        if x>y:
            s+= self.name + ' is more likely to have come from ' + source1.name
        elif y>x:
            s+= self.name + ' is more likely to have come from ' + source2.name
        elif x == y:
            s+= self.name + ' is equally likely to have come from either ' + source1.name + ' or ' + source2.name
        print (s)
        
        
        
def stem(s):
    """That accepts a string as a parameter. The function should 
   then return the stem of s. The stem of a word is the root part 
   of the word, which excludes any prefixes and suffixes.
   """
    len_word = len(s)
    if len_word <=3:
        return s
    elif s[-3:] == 'ing':
        new_stem = s[:-3]
    elif s[-3:] == 'ing' and s[-4] == s[-5]:
        new_stem = s[:4]
    elif s[-1] == 'y':
        new_stem = s[:-1] + 'i'
    elif s[-3:] == 'ies':
        new_stem = s[:-2]
    elif s[0:2] == 'un':
        new_stem = s[2:]
    elif s[0:3] == 'pre':
        new_stem = s[3:]
    elif s[-1] == 'e':
        new_stem = s[:-1]
    elif s[-2:] == 'er':
        new_stem = s[:-2] 
    elif s[-3:] == 'ers':
        new_stem = s[:-3]
    else:
        return s
    return new_stem
        
   


def clean_text(text):
    """takes the text from a file and splits it to its individual words,
    removes punctuation, and makes it lowercase
    """
    for symbol in """.,?"'!;:""":
        text = text.replace(symbol,'')
    clntxt1 = text.lower()
    clntxt2 = clntxt1.split()
    return clntxt2


def compare_dictionaries(d1,d2):
    """docstring"""
    if d1 == {}:
        return -50
    log_sim_score = 0
    total = 0 
    for x in d1:
        total += d1[x]
    for word in d2:
        if word in d1:
            prob = d1[word]/total
            log_sim_score += d2[word]*(math.log(prob))
        else:
            log_sim_score += d2[word]*(math.log(.5/total))
    return log_sim_score


# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def run_tests():
    """ your docstring goes here """
    source1 = TextModel('Wash_Post')
    source1.add_file('Wash_Post_Covid.txt')

    source2 = TextModel('The_Economist')
    source2.add_file('The_Econ.txt')

    new1 = TextModel('NYT')
    new1.add_file('New_York_Times_Covid.txt')
    new1.classify(source1, source2)

    # Add code for three other new models below.
    new2 = TextModel('BBC')
    new2.add_file('BBC_Covid.txt')
    new2.classify(source1,source2)
    
    new3 = TextModel('ABC')
    new3.add_file('ABC_Covid.txt')
    new3.classify(source1,source2)
    
    new4 = TextModel('Guardian')
    new4.add_file('Guardian_Covid.txt')
    new4.classify(source1,source2)