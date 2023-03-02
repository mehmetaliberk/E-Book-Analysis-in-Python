import requests
from bs4 import BeautifulSoup
import operator

x = str(input("please enter the name of the first book: ")).replace(" ","_")#taking name of the book from user
url = ("https://en.wikibooks.org/wiki/" + x.replace("'", "%27")+ "/Print_version")#mimicing the link by replacing some symbols
response = requests.get(url)#Making a request with Requests
y=int(input("how many word frequencies do you wish to see ? "))#asking user for number of frequencies
html = response.content#content type


soup = BeautifulSoup(html,"html.parser")#getting html code as unicode characters

WORDS = list()
#list of stopwords
STOPWORDS = ["me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", 
             "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
             "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
             "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", 
             "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", 
             "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
             "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
             "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", "don", "should", "now"]
#list of symbols to be removed
SYMBOLS = [",",".","?",".","é","!","'","^","+","%","&","/","=","?",
           "_","<",">","£","#","$","½","{","[","]","}","|","@","-",
           "*",":",";","æ","ß","1","2","3","4","5","6","7","8","9","0","(", ")" ,"\\",'"',"'","~"]


def REM_STOP_WORDS(WORDS):#function to remowing stop words
    CLEAN_WORDS = list()
    for WORD in WORDS:#taking words list as a reference(words list=book)
        if WORD not in STOPWORDS:#checking every word in the list of the stopwords to see if we have stopword to remove
            if len(WORD) > 1 :# I also added these because theres no 1 digit meaningful characters
                CLEAN_WORDS.append(WORD)#appending clean words to list of clean words
    return CLEAN_WORDS

def REM_SYMB(CLEAN_WORDS):#function to remove symbols
   W_SYMB_WORDS=list()
   for WORD in CLEAN_WORDS:#taking clean words list as a reference
      for SYMB in SYMBOLS:
         if SYMB in WORD:
            SYMB_index=WORD.index(SYMB)#I checked index to remove all symbols from words
            WORD=WORD.replace(SYMB,"")#replacing symbols
            WORD=WORD[0:SYMB_index]#I found the index of symbols and took the word up there
      if(len(WORD)>1):#i did this trick here too
         W_SYMB_WORDS.append(WORD)#appending clean words to cleanest list
   return  W_SYMB_WORDS

def DICT(CLEAN_WORDS):#function to adding words and their freqs to a dictionary
    WORD_NUMB = dict()
    for WORD in CLEAN_WORDS:#taking clean words as a reference
        if WORD in WORD_NUMB:#checking dict for words
            WORD_NUMB[WORD] += 1#if any repeat occurs the counter goes up
        else:
            WORD_NUMB[WORD] = 1#if a words appear as a first time it will start counter
    return WORD_NUMB
        
    

with open ("book1.txt","w", encoding = "UTF-8") as file:#opening text file for first book
   for i in soup.find_all("div",{"mw-parser-output"}):#scanning entire document and looking for correct book parts
       file.write(i.text)#writing text to a file
   

with open("book1.txt","r", encoding = "UTF-8") as file:#reading from text file
   ALL_WORDS = file.read()
   ALL_WORDS_LIST = ALL_WORDS.lower().split()#spliting words
   for WORD in ALL_WORDS_LIST:
       WORDS.append(WORD)#appending words to the list


CLEAN_WORDS = REM_STOP_WORDS(WORDS)#using functions to clean and append words to a dictionary
CLEAN_WORDS=REM_SYMB(CLEAN_WORDS)#using functions to clean and append words to a dictionary
WORDS = DICT(CLEAN_WORDS)#using functions to clean and append words to a dictionary
a=0
print("frequencies of book1")
print("NO WORD FREQ")
for key,value in sorted(WORDS.items(), key = operator.itemgetter(1), reverse=True):#printing frequencies with operator library in order
    print(str(a+1)+". "+key,value)
    a=a+1
    if (a==y):
        break

#same operations for second book is below
x = str(input("please enter the name of the second book to continue(this option includes both common and distinct words): ")).replace(" ","_")
url = ("https://en.wikibooks.org/wiki/" + x.replace("'", "%27")+ "/Print_version")
response = requests.get(url)

html = response.content


soup = BeautifulSoup(html,"html.parser")

WORDS2 = list()


with open ("book2.txt","w", encoding = "UTF-8") as file:
   for i in soup.find_all("div",{"mw-parser-output"}):
       file.write(i.text)
   

with open("book2.txt","r", encoding = "UTF-8") as file:
   ALL_WORDS2 = file.read()
   ALL_WORDS_LIST2 = ALL_WORDS2.lower().split()
   for WORD2 in ALL_WORDS_LIST2:
       WORDS2.append(WORD2)


CLEAN_WORDS2 = REM_STOP_WORDS(WORDS2)
CLEAN_WORDS2=REM_SYMB(CLEAN_WORDS2)
WORDS2 = DICT(CLEAN_WORDS2)
a=0
print("frequencies of book2")
print("NO WORD FREQ")
for key,value in sorted(WORDS2.items(), key = operator.itemgetter(1), reverse=True):
    print(str(a+1)+". "+key,value)
    a=a+1
    if (a==y):
        break
    
print("\n")    
WORDS2 = list()
WORDS3=CLEAN_WORDS+CLEAN_WORDS2#summing the two seperate list of books
WORDS3=DICT(WORDS3)#turning sum list to dictionary


a=0
print("frequencies of common words")
print("NO WORD FREQ")
for key,value in sorted(WORDS3.items(), key = operator.itemgetter(1), reverse=True):# printing sum of the freqs 
    print(str(a+1)+". "+key,value)
    a=a+1
    if (a==y):
        break    
    
print("\n") 
WORDS4=list()
for WORDS in CLEAN_WORDS:
    if WORDS not in CLEAN_WORDS2:#checking the list for distinct words
        WORDS4.append(WORDS)#appending discint words
        
WORDS4=DICT(WORDS4)#turning distinct list to dictionary
        
a=0
print("frequencies of distinct words(book1-book2)")
print("NO WORD FREQ")
for key,value in sorted(WORDS4.items(), key = operator.itemgetter(1), reverse=True):#printing distinct library
    print(str(a+1)+". "+key,value)
    a=a+1
    if (a==y):
        break    

print("\n") 
#same process goes for other distinct word list
WORDS5=list()
for WORDS in CLEAN_WORDS2:
    if WORDS not in CLEAN_WORDS:
        WORDS5.append(WORDS)
        
WORDS5=DICT(WORDS5)
        
a=0
print("frequencies of distinct words(book2-book1)")
print("NO WORD FREQ")
for key,value in sorted(WORDS5.items(), key = operator.itemgetter(1), reverse=True):
    print(str(a+1)+". "+key,value)
    a=a+1
    if (a==y):
        break    