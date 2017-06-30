# DOIPress
## Richard Ostler
## 30/06/2017, Rothamsted Research

A very simple Python GUI which generates a new random String DOI and logs the result to a database.

To use:
1. Generate a database table using the DOIManagaer.sql table script in the sql folder. This table is used for logging the generated DOI and recording seed and creation information.

2. Create and populate a config.ini with the following:
```
[DATABASE]
host=...
user=...	
password=...
db=DOI_...

[DOI]
prefix=...Your Organisation's DOI prefix
```
3. Run the program.

The file setup.py can be used for compiling a distributable MSI by navigating to the project DOIPress folder using the following command:
> python setup.py bdist_msi
