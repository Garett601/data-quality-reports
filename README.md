# README #


### What is this repository for? ###

* Quick summary:
	* This python script automatically generates Data Quality Reports for your dataset.
	* It can be used on raw data to identify erroneous data or features that do not add predictive value.

This function can be run before, during and after data pre-processing to make sure your final dataset is a good quality dataset for model training.
* Version:
	* V1.0.1

### How do I get set up? ###

* Summary of set up:
	* Clone the repository
	* Use the dqr.ipynb to perform run the Data Quality Report on your data
		* Make sure to update the file_path variable to the file_path of your data
			* file_path = '<YOUR FILE PATH>'
		* Change the DataFrame creation code to match your file type
	* You can export and save your Data Quality Reports to csv files by specifying the save_as_csv argument to True
		* The default behavivour is save_as_csv = False
		* This results in the Data Quality Report being printed to the screen in a Jupyter Notebook
* Dependencies:
	* pandas
	* numpy

### Contribution guidelines ###

* If there are any change requests or ways in which this function can be improved, please contact me as I am still learning and would love to learn how to make my code better and more efficient.

### Who do I talk to? ###

* Repo owner or admin:
	* Garett Sidwell

### Updates ###

* 09/11/2022: Created V1.0.1
	* Updated the dqr function in data_quality_report.py to allow the option to save csv files or not
	* Added dqr.ipynb Jupyter Notebook to quickly perform Data Quality Check after specifying file_path
