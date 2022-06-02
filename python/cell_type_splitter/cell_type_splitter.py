import sys
import pandas as pd
from tqdm import tqdm

def ingest_data_from_tsv(read_path):
	print(f'Reading file: {read_path}')
	root_df=pd.read_csv(read_path, sep='\t')
	tqdm.pandas(desc='Ingesting data...nom...nom...nom')
	root_df.progress_apply(lambda x: x)
	return root_df
	
def get_cell_types_from_df(root_df):
	print('Getting cell types from dataframe')
	header=root_df.head(0)
	header.iloc[: , 1:].columns
	cell_types=[]
	for c in header:
		c_cleaned = c.split('.', 1)[0]
		if c_cleaned not in cell_types and c_cleaned != 'Gene':
			cell_types.append(c_cleaned)
	return cell_types
	
def create_tsv_from_cell_type(cell_type, root_df, write_path):
	print(f'Creating dataframe for {cell_type}')
	file_name=f'{write_path}/{cell_type}.txt'
	first_col=root_df.filter(['Gene'], axis=1)
	cell_df=root_df.filter(like=cell_type, axis=1)
	cell_df.insert(0, "Gene", first_col.values , True)
	print(f'''Output dataframe to file: {file_name} : 
	{cell_df}''')
	cell_df.to_csv(file_name, sep="\t", index=False)

def main():
	print('Kicking off the cell splitter - be patient, this might take a while...')
	if len(sys.argv) != 3:
		raise Exception("Invalid number of arguments, please pass the following arguments: <input_file_path> <output_folder_path>")
	read_path=str(sys.argv[1])
	write_path=str(sys.argv[2])
	root_df=ingest_data_from_tsv(read_path)
	cell_types=get_cell_types_from_df(root_df)
	for c in cell_types:
		create_tsv_from_cell_type(c, root_df, write_path)
		
if __name__ == "__main__":
    main()

# run this to use:
# python cell_type_spliiter.py <input_file_path> <output_folder_path>
# note, ingest_data_from_tsv can take a long time to read data from a large file, just wait it out
