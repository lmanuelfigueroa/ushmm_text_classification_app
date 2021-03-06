import streamlit as st
from spacy.lang.en import English
import operator
import spacy
from io import StringIO


tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

def app() -> None:
    st.title("Upload Corpus")

    upload_files = st.file_uploader("Enter a file:",accept_multiple_files=True)

    if upload_files is not None:
        for file in upload_files:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            process_document(string_data,file.name)
        st.write(f"Done Processing Documents")
        

#processing each file uploaded 
def process_document(document,file_name) -> None:

    nlp = English()
    PERCENTAGE_CONSIDER_TAG = 0
    label_dict = dict.fromkeys(tags,0)
    nlp_labels = spacy.load("model_output_exclusive/model-last")
    
    if nlp.pipe_names != []:
        nlp.remove_pipe("sentencizer")

    nlp.max_length = 174214790
    nlp.add_pipe('sentencizer')
    doc = nlp(document, disable=['parser', 'tagger', 'ner'])

    num_of_sentences = len(list(doc.sents))

    num_of_tags_found = 0
    st.write(f"Loading Results for {file_name}\n")

    #processing each sentence and getting the tag for each sentence with the highest percentage
    for sent in doc.sents:
        text = remove_accents(str(sent.text))
        doc = nlp_labels(text)
    
        first_tag = top_tag(doc.cats)

        #creating a threshold to count how many sentences have a valuable tag associated
        if doc.cats[first_tag] > PERCENTAGE_CONSIDER_TAG:
            num_of_tags_found +=1
            label_dict[first_tag] = label_dict[first_tag] + 1
    
    
    #st.write(f"Document {file_name} contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned on {round(PERCENTAGE_CONSIDER_TAG*100,1)}% tag requirement\n")
    st.write(f"Document contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned")
    
    #getting the percentage of tags for the document
    for tag in label_dict:
        label_dict[tag] = round(label_dict[tag]*100/num_of_tags_found,1)

    print_top_tags(label_dict)


#function sorts the tags with highest on the front and prints the top 5 tags in the dictionary 
def print_top_tags(tags: dict) -> None:

    NUMB_OF_TAGS = 5
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    top_tags = []
    
    for _ in range(NUMB_OF_TAGS):
        pair = next(pair_iter)
        top_tags.append(pair)


    clean_tags = clean_results(top_tags)
    st.write(f"The top { NUMB_OF_TAGS} tags in the document are {clean_tags}\n")

# used to print the results more visually pleasing for user by capitalizing the name of the tag and adding percent sign to float value
def clean_results(results):

    clean_results = []
    
    for item in results:
        clean_results.append((item[0].capitalize(),str(item[1]) + "%" ))
    return clean_results

#gets the tag with the highest percent value
def top_tag(tags : dict) -> str:
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)
    pair = next(pair_iter)
    return pair[0]

def remove_accents(text):
    #Polish letters
    letters= {
    '??':'l', '??':'a', '??':'n', '??':'c', '??':'o', '??':'e', '??':'s', '??':'z', '??':'z',
    '??':'L', '??':'A', '??':'N', '??':'C', '??':'O', '??':'E', '??':'S', '??':'Z', '??':'Z',

    #Accent Vowels
    "??":"a", "??":"a", "??":"a", "??":"a", "??":"a", "??":"a", "??": "ae",
    "??":"A", "??":"A", "??":"A", "??":"A", "??":"A", "??":"A", "??": "ae",

    "??":"e", "??":"e", "??":"e", "??":"e",
    "??":"E", "??":"E", "??":"E", "??":"E",

    "??":"i", "??":"i", "??":"i", "??":"i",
    "??":"I", "??":"I", "??":"I", "??":"I",

    "??": "o", "??": "o", "??": "o",  "??": "o",  "??": "o", "??": "o",
    "??": "O", "??": "O", "??": "O",  "??": "O",  "??": "O", "??": "O",

    "??": "u", "??": "u",  "??": "u",  "??": "u",
    "??": "U", "??": "U",  "??": "U",  "??": "U",

    "??": "y", "??": "y",
    "??": "Y", "??": "Y",

    #Accent Cononants
    "??": "c", "??": "C",
    "??": "ss"
    }
    trans=str.maketrans(letters)
    result=text.translate(trans)
    return (result)
