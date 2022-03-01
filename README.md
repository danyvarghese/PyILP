# PyILP
A novel user-friendly Python/Jupyter interface for Inductive Logic programming(ILP)  system for teaching relational machine learning and comparing different algorithms.

We have incoperated two different ILP algorithms in this packge
1) Aleph
2) Metagol

# Aleph
Aleph is an Inductive Logic Programming (ILP) system developed by Ashwin Srinivasan: http://www.cs.ox.ac.uk/activities/machlearn/Aleph/

In this package we use a porting of Aleph v.5 to SWI-Prolog prepared by Fabrizio Riguzzi: https://github.com/friguzzi/aleph

# Metagol
Metagol is an Meta-Interpretive Learning (MIL) system maintained by Andrew Cropper: https://github.com/metagol/metagol

# Requirements
[SWI-Prolog](https://www.swi-prolog.org/)

[pyswip](https://pypi.org/project/pyswip/)

# Usage
## Aleph - Hold-out
The following fuction will help you to perfom hold-out test using aleph.

```python
aleph_learn(file="BK.pl", 
            test_size=0.33, 
            positive_example="pos_example.f", 
            negative_example="neg_example.n", 
            shuffle=False, 
            settings=[])
```
| Parameter  | Explanation |
| ------------- | ------------- |
| file  | **Default** : ***BK.pl*** <br> Allows to input background information. You can include aleph parameters in the file, if so dont input the parameter *settings*  |
| test_size  | **Default** : ***0.33*** <br> should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split |
| positive_example | **Default** : ***pos_example.f*** <br>  Allows to input the positive example|
| negative_example | **Default** : ***neg_example.n*** <br>  Allows to input the negative example|
|shuffle|**Default** : ***False*** <br> Whether or not to shuffle the data before splitting|
|settings | **Default** : ***[]*** <br>  Allows to include aleph parameters as file format|



