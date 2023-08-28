import os

class InvertedIndex:
    """This class represents an inverted index. It can be used to save and load an inverted index from a file.
    """
    def __init__(self, persistent_file_path = None):
        """Constructor for the InvertedIndex class. It can load an index from a file or create a new one.

        Args:
            persistent_file_path (string/path, optional): A file path for index. Defaults to None.

        Raises:
            Exception: The given file doesn't exist!
            Exception: Index couldn't be loaded, the given file is corrupted!
        """
        if persistent_file_path is None:
            self.index = {}
        elif os.path.exists(persistent_file_path):
            
            try:
                # Load the index from the file
                with open(persistent_file_path, "r") as file:
                    self.index = {}
                    for line in file:
                        token, postings = line.split("=")
                        self.index[token] = {}
                        for posting in postings.split(";"):
                            stripped_posting = posting.strip()
                            if stripped_posting != "":
                                doc_id, position = stripped_posting.split(":")
                                
                                position_list = map(int, position.split(","))
                                self.index[token][int(doc_id)] = list(position_list)
            except:
                raise Exception("[ERROR] Couldn't load the index, the given file is corrupted!")
        else:
            raise Exception("[ERROR] Couldn't load the index, the given file doesn't exist!")
        
    def save(self, file_name):
        """This function saves the index to a file.

        Args:
            file_name (str): Takes an absolute or relative path to a file.
        """
        with open(file_name, "w") as file:
            # file.write(str(self.total_tokens) + "\n")
            for token in self.index:
                file.write(token + "=")
                for doc_id in self.index[token].keys():
                    
                    file.write(str(doc_id) + ":")
                    temp_position_write = ",".join(map(str, self.index[token][doc_id]))

                    file.write(temp_position_write + ";")
                file.write("\n")
            
            print("[INFO] Index saved to file: " + file_name)
                
    def setup(self, data: dict):
        """This function sets up the index from a dictionary.

        Args:
            data (dict): A dictionary that contains tokens as keys and a dictionary of document IDs and positions as values.
        """
        
        # Sort the dictionary by the keys
        sorted_data = {key:data[key] for key in sorted(data)}


        # Merge the dictionaries
        merged_dictionary = {}
        for key in sorted_data:
            for token in sorted_data[key]:
                
                # If the token is already in the merged dictionary, add the document ID and positions to it
                if token in merged_dictionary:
                    merged_dictionary[token][key] = sorted_data[key][token]
                else:
                    merged_dictionary[token] = {key: sorted_data[key][token]}
        
        # Sort the dictionary by the keys
        self.index = {key:merged_dictionary[key] for key in sorted(merged_dictionary)}