import os
import re
import sys
from utils import tokenize
from InvertedIndex import InvertedIndex

                
def corpus_statistics(index: InvertedIndex):
    unique_tokens = len(index.index.keys())
    total_tokens = 0
    
    frequency_dict = {}
    for token in index.index:
        for doc_id in index.index[token]:
            if token in frequency_dict:
                total_tokens += len(index.index[token][doc_id])
                frequency_dict[token] += len(index.index[token][doc_id])
            else:
                total_tokens += len(index.index[token][doc_id])
                frequency_dict[token] = len(index.index[token][doc_id])

    sorted_freq_dict = {k: v for k, v in sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)}
        
    for i in range(0, 100):
        print(f"{list(sorted_freq_dict.keys())[i]}: {list(sorted_freq_dict.values())[i]}")
                
    print(f"Unique tokens: {unique_tokens}")
    print(f"Total tokens: {total_tokens}")
    


def main(dataset_path, index_path = "", index_name = "documents.index", stats = False):
    
    print("[INFO] Preparing for indexing...")
    
    # Initialize the index object
    inverted_index = InvertedIndex()
    index_dictionary = {}
    
    # Create the save path from string
    save_path = os.path.abspath(os.path.join(index_path, index_name))
    
    print("[INFO] Loading dataset...")
    try: 
        
        # Check if the given path is a directory
        if not os.path.isdir(dataset_path):
            raise Exception("[ERROR] The given dataset path is not a directory!")
        
        # Iterate over the files in the directory
        for root, _, files in os.walk(os.path.join(dataset_path)):
            for i, file in enumerate(files):
                if file.endswith(".sgm"):
                    
                    print(f"\r[INFO] Processing file {i+1}/{len(files)}...", end="\r")
                    
                    # Read the file
                    current_file = open(os.path.join(root, file), "r", encoding="latin-1")
                    
                    # Split the file into articles
                    articles = re.split(r'</REUTERS>', current_file.read())

                    # Iterate over the articles
                    for article in articles:
                        
                        # Remove starting and ending whitespaces
                        target_article = article.strip()
                        
                        # Remove end of text characters
                        latin1_special_characters = "&#3"
                        target_article = target_article.replace(latin1_special_characters, "")
                        
                        # If article is empty, skip it
                        if target_article == "":
                            continue
                        
                        # Get the ID of the article
                        new_id = int(re.search(r'NEWID="(\d+)"', target_article).group(1))
                        
                        # Parse the content of the article
                        corpus = ""
                        text_part = re.search(r'<TEXT(.+)</TEXT>', target_article, re.DOTALL).group(1)
                        if title := re.search(r'<TITLE>(.+)</TITLE>', text_part, re.DOTALL):
                            corpus += title.group(1)
                        
                        if body := re.search(r'<BODY>(.+)</BODY>', text_part, re.DOTALL): 
                            corpus += " " + body.group(1)

                        # Tokenize the content of the article
                        tokenized_content = tokenize(corpus)
                        
                        # Create the dictionary and position list for the article
                        article_tokens_positional = {}
                        for position, token in enumerate(tokenized_content):
                            if token in article_tokens_positional:
                                article_tokens_positional[token].append(position)
                            else:
                                article_tokens_positional[token] = [position]

                        # Add the article to the dictionary
                        index_dictionary[new_id] = article_tokens_positional
                        
        print(f"\r[INFO] All files are succesfully processed. Now saving the index to {save_path}...")
            
        # Setup the index and save it
        inverted_index.setup(index_dictionary)
        inverted_index.save(save_path)
        
        if stats:
            corpus_statistics(inverted_index)
        
    except Exception as e:
        quit(e)
        
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        quit("Usage: python index_builder.py <dataset_path> <index_path> <index_name>")
    
    main(dataset_path=sys.argv[1], index_path=sys.argv[2], index_name=sys.argv[3])
                    