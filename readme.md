## Requirements
- Python 3.9+

## How to Run

> Before running the query processor `(search.py` module, you should run the indexer module to ensure there is an index created. Otherwise the query processor module will not run.

### Indexer Module

The indexer module takes 3 arguements, these arguements are:

- **<dataset_folder_path>:** This arguements is for selecting the location of the dataset folder
- **<index_save_folder_path>:** This arguement takes a path to a folder which will store the index file
- **<index_filename>:** This arguement is for setting the index files's name


So the module can be run with the following command with parts between <> replaced with necessary input:

```bash
python index_builder.py <dataset_folder_path> <index_save_folder_path> <index_filename>
```

After indexer is run succesfully it will output the absolute path for the created index. Then you can plug it in for running the query processor.

### Query Processor Module

Running the query processor takes one user arguement:

- **<index_file_path>:** This arguement is pointing to created index's path, you should fill it with the result of the indexer module.

The following command will run the query processor module:

```bash
python search.py <index_file_path>
```

After the module is started it will prompt the user for input, for these a few assumptions are made:

1. Phrase queries start and end with quotes ("test query")
2. If a query starts with quote (") then the program will search for ending quote, if it is not found it will output an error message. So for positional queries please don't use a " at the start.
3. Positional queries' 2nd word would be a constant **positive** number since the distance is two sided.