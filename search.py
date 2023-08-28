import sys
import os

from InvertedIndex import InvertedIndex
from utils import tokenize

def positional_search(index: InvertedIndex, query: str, strict_order = False) -> list:
    """This function searches for documents that contain the tokens in the query with the required distance. 
    The search is positional and the order of the tokens is not strict by default.

    Args:
        index (InvertedIndex): Takes an inverted index as an input
        query (str): positional query
        strict_order (bool, optional): Parameter for deciding if the order of the tokens in query is strict. Defaults to False.

    Returns:
        list: A list of document IDs that contain the tokens in the query with the required distance
    """
    # Tokenize the query
    tokenized_query = tokenize(query)
    
    max_distance = int(tokenized_query[1])
    
    
    # If the query doesn't contain the required tokens, return an empty list
    if tokenized_query[0] not in index.index or tokenized_query[2] not in index.index:
        return []
    
    # Get the documents that contain the first and the second token
    documents_containing_arg1 = index.index[tokenized_query[0]].keys()
    documents_containing_arg2 = index.index[tokenized_query[2]].keys()
    
    # Get the documents that contain both tokens
    possible_documents = [doc_id for doc_id in documents_containing_arg1 if doc_id in documents_containing_arg2]
        
    
    confirmed_documents = []
    
    # Iterate over the documents that contain both tokens
    for doc_id in possible_documents:
        
        document_contains = False
        
        # Get the positions of the tokens in the document
        first_token_positions = index.index[tokenized_query[0]][doc_id]
        second_token_positions = index.index[tokenized_query[2]][doc_id]
        
        # Select the range of positions that are allowed
        available_range = range(-max_distance-1, max_distance + 2)
        if strict_order:
            available_range = range(1, max_distance + 2)
        
        # Iterate over the positions of the first token
        for start_position in first_token_positions:
            for i in available_range:
                
                # If the position is negative, skip it
                if i == 0 or start_position + i < 0:
                    continue
                
                # If the second token is found in the document, break and set the document_contains flag to True
                if start_position + i in second_token_positions:
                    document_contains = True
                    break
                
            if document_contains:
                break
        
        # If the document contains the tokens with the required distance, add it to the confirmed documents
        if document_contains:
            confirmed_documents.append(doc_id)
                        
    return confirmed_documents
            
    


def phrase_search(index: InvertedIndex, query: str) -> list:
    """This function searches for documents that contain the phrase in the query. The search is exact and the order of the tokens is strict.
    
    Args:
        index (InvertedIndex): An inverted index object
        query (str): A phrase query starting and ending with double quotes

    Returns:
        list: A list of document IDs that contain the phrase in the query
    """
    
    # Remove the double quotes from the query and tokenize it
    tokenized_query = tokenize(query)
    
    if len(tokenized_query) == 1:
        if tokenized_query[0] in index.index:
            return list(index.index[tokenized_query[0]].keys())
    
    
    possible_documents = []
    
    # Iterate over the query tokens
    for i in range(len(tokenized_query)):
        
        # If the last token is reached, break
        if i == len(tokenized_query) - 1:
            break
        
        # Use the positional search to find the documents that contain the current token and the next one with a distance of 0
        # the ordering of the tokens is important
        temp_documents = positional_search(index, tokenized_query[i] + " 0 " + tokenized_query[i+1], strict_order=True)
        
        # If this is the first iteration, set the possible documents to the documents that contain the first two tokens
        if i == 0:
            possible_documents = temp_documents
        else: # Otherwise, keep only the documents that contain the current token and the next one
            possible_documents = [doc_id for doc_id in possible_documents if doc_id in temp_documents]
    
    return possible_documents


def main(index_path = None):
    
    try:
        # If the index path is not given, quit with error
        if index_path == None:
            raise Exception("[ERROR] No index file was given!")
        if not(os.path.exists(index_path)) or not(os.path.isfile(index_path)):
            raise Exception("[ERROR] The given index file doesn't exist!")

        # Load the index
        print("[INFO] Loading index...")
        inverted_index = InvertedIndex(persistent_file_path=index_path)
        print("Welcome to the query searcher! If you want to quit please type ':quit'")
        
        # Start the query loop
        while True:
            user_input = input("Please enter your query: ").strip()
            
            if user_input == ":quit":
                print("Thank you for using the query searcher! Goodbye!")
                break
            
            # If the query is a phrase query, use the phrase search (starts with quotes and ends with quotes)
            if user_input.startswith('"'):
                if user_input.endswith('"'):
                    
                    search_results = phrase_search(inverted_index, user_input)
                    if len(search_results) == 0:
                        print("No documents were found to match your query!\n")
                        continue
                    
                    result_string = ", ".join(map(str, search_results))
                    print (f"The following {len(search_results)} documents were found matching your query: {result_string}\n")
                    
                else: # If the query doesn't end with quotes, it's invalid
                    print ("\n[Error] Invalid query! Remember to close the quotes at the end of the query!\n")
            else:      
                split_query = user_input.split()      
                
                if len(split_query) == 3 and split_query[1].isnumeric():    
                    search_results = positional_search(inverted_index, user_input)
                    
                    if len(search_results) == 0:
                        print("No documents were found to match your query!\n")
                        continue
                    
                    result_string = ", ".join(map(str, search_results))
                    
                    print (f"The following {len(search_results)} documents were found matching your query: {result_string}\n")
                else:
                    print("\n[ERROR] Invalid query! Please try again. The example queries are as follows:")
                    print("1. Positional query: 'apple n banana' with n being the number of words between the two words(can be 0 or more)")
                    print('2. Phrase query: "apple banana" (the words must be in the same order and they must be inside double quotes "")\n')
    except Exception as e:
        quit(e)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        quit("[ERROR] Invalid number of arguments! Please provide the path to the index file as an argument! (e.g. python search.py index_file.index)")