# README #

## Data Quality Reports (DQR)

This repository contains a Python class DQR for generating Data Quality Reports on pandas DataFrames. The class performs an analysis on the DataFrame and divides the data into continuous and categorical variables, creating reports with relevant statistical metrics for both types.

### Version:
* V0.1.0

### Dependencies:
All dependencies are handled by the poetry package. Check the pyproject.toml for more information

### Contribution guidelines ###

* If there are any change requests or ways in which this function can be improved, please contact me as I am still learning and would love to learn how to make my code better and more efficient.

### Who do I talk to? ###

* Repo owner or admin:
	* Garett Sidwell

### Updates

* 09/11/2022: Created V1.0.1
	* Updated the dqr function in data_quality_report.py to allow the option to save csv files or not.
	 * Added dqr.ipynb Jupyter Notebook to quickly perform Data Quality Check after specifying file_path.

* 17/07/2023: Created V0.1.0
	* Changed package structure to conform to PEP guidelines.
	* Changed versioning scheme to represent new structure and to follow the MAJOR.MINOR.PATCH convention.
	* Converted implementation to a Class to make the code easier to understand and to implement only the methods required by the user.
