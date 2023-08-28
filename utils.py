import string

def tokenize(input):
    
    punctuation_removed_content = input.translate(str.maketrans('', '', string.punctuation))
    
    lowercased_content = punctuation_removed_content.lower()
    tokenized_content = lowercased_content.split()

    return tokenized_content