from keras.preprocessing.sequence import pad_sequences
from re import sub
import string
# # the 5 lines below need to be run once to download relevant nltk content
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk import tokenize
from nltk.corpus import stopwords



class BaseTextCleaner:
    STOPWORDS = set(stopwords.words('english'))
    PUNCTUATION = {i for i in string.punctuation}
    
    @staticmethod     
    def split_sentence_to_list_of_words(sentence):
        return tokenize.word_tokenize(sentence)
    
    @classmethod
    def split_article_to_lists_of_words(cls, article):    
        article_sentences = tokenize.sent_tokenize(article)
        article_words = [cls.split_sentence_to_list_of_words(sentence) for sentence in article_sentences]
        return article_words   
    
    @classmethod
    def lemmatize_and_denoise_sentence(cls, sentence):
        cleaned_sentence = []
        lemmatizer = WordNetLemmatizer()
        for word, tag in pos_tag(sentence):
            word = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', word)
            word = sub(r"(@[A-Za-z0-9_]+)","", word)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            word = lemmatizer.lemmatize(word, pos)

            if len(word) > 0:
                if word not in cls.PUNCTUATION:
                    if word.lower() not in cls.STOPWORDS:
                        cleaned_sentence.append(word.lower())
        return cleaned_sentence
    
    @classmethod
    def lemmatize_and_denoise_article(cls, article):
        return [cls.lemmatize_and_denoise_sentence(sent) for sent in article]
    
    @staticmethod
    def sentence_to_sequences(sentence, tokenizer):
        return tokenizer.texts_to_sequences([sentence])   
    
    @classmethod
    def article_to_sequences(cls, article, tokenizer):
        return [cls.sentence_to_sequences(sent, tokenizer) for sent in article]
    
    @staticmethod
    def pad_sentence(sentence, padding_type, max_length, trunc_type):
        return pad_sequences(sentence, padding=padding_type, maxlen=max_length, truncating=trunc_type)
    
    @classmethod
    def pad_article(cls, article, padding_type, max_length, trunc_type):
        return [cls.pad_sentence(sent, padding_type=padding_type, max_length=max_length, trunc_type=trunc_type) for sent in article]


         
class ArticleTextCleaner(BaseTextCleaner):
    
    def __init__(self, trunc_type='post', max_length=100, padding_type='post', tokenizer=None):
        assert tokenizer != None
        self.tokenizer = tokenizer
        self.trunc_type = trunc_type
        self.max_length = max_length
        self.padding_type = padding_type

    def get_cleaned_element(self, element):
        sentences = tokenize.sent_tokenize(element)

        element_words = self.split_article_to_lists_of_words(element)
        element_sentences = [' '.join(sent) for sent in element_words]
        element_denoized = self.lemmatize_and_denoise_article(element_words)
        element_sentences = [' '.join(sent) for sent in element_denoized] # join words back into sentence after cleaning (sequencing works on sentence strings)
        element_sequences = self.article_to_sequences(element_sentences, self.tokenizer) # using tokenizer to convert lists of words into lists of numbers
        element_padded_sequences = self.pad_article(element_sequences, self.padding_type, self.max_length, self.trunc_type) # padding the lists of numbers with zeros to match dimensions of the NN
        return sentences, element_padded_sequences


def convert_result_from_list_to_label(row):
    if (row[0][0] > 0.33) & (row[0][0] > row[0][2]): # positive > 0.33 and positive > negative
        return 1
    elif (row[0][2] > 0.33) & (row[0][2] > row[0][0]): # negative > 0.33 and negative > positive
        return -1
    else:
        return 0