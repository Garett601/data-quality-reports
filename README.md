# README #


### What is this repository for? ###

* Quick summary:
	* This python script automatically generates Data Quality Reports for your dataset.
	* It can be used on raw data to identify erroneous data or features that do not add predictive value.

This function can be run before, during and after data pre-processing to make sure your final dataset is a good quality dataset for model training.
* Version:
	* V1.0.0

### How do I get set up? ###

* Summary of set up:
	* Make sure 'data_quality_report.py' is in your working folder.
	* from data_quality_report import dqr
	* df = pd.read_csv('file_path')
	* continuous_data, categorical_data = dqr(df)
	* This function will create a csv file as an output for both continuous and categorical data.
	* If you are using a Jupyter Notebook, you can use:
		* display(continuous_data)
		* display(categorical_data)
* Dependencies:
	* pandas
	* numpy

### Contribution guidelines ###

* If there are any change requests or ways in which this function can be improved, please contact me as I am still learning and would love to learn how to make my code better and more efficient.

### Who do I talk to? ###

* Repo owner or admin:
	* Garett Sidwell
