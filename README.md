## Synopsis

These classes implement the Graph-Based Diagnostic Medical Decision Support System found [here](http://www.infosecanalytics.com/files/Graph-Based_Diagnostic_Medical_Decision_Support_System-Rev_NEW-DRAFT.pdf)

This code implements three novel inventions:

1. A module for the generation of statistically varying medical records with configurable accuracy, number of signs, and number of symptoms. This is implemented in the synthetic.py module.
2. An algorithm for training a new machine learning model for analysis of competing hypotheses, (the Bassett-Deitmen Training Algorithm).  This is implemented in the model.py module.
3. An algorithm for querying the model, (the Bassett-Deitman Query Algorithm), is provided for querying trained models.  it is also implemented in the model.py module.


This will generate training records, train the model on them, and provide a web interface on port 8080.  A new record to diagnose can be generated by visiting [http://localhost:8080/records/?record_count=1](http://localhost:8080/records/?record_count=1).  The diagnostic UI is located at [http://localhost:8080/](http://localhost:8080/).  Enter the signs and symptoms, click the 'diagnose' button, and you should be provided an output similar to:
![Bassett Deitmen Diagnostic MDSS UI](http://www.infosecanalytics.com/images/dmdss_ui.png)






Three APIs exist within the UI.
### Record Generation API
The record generation API exists at `localhost:8080/records/`.  It takes an argument of ```record_count``` with the number of records requested and returns them as a JSON dictionary of the form:
```
 'signs': {'sign_1404': 0.1},
 'symptoms': {'symptom_11': 0.5,
 'symptom_24': 0.3,
 'symptom_72': 1,
 'symptom_80': 0}},
{'diagnosis': 'diagnosis_4789',
 'signs': {'sign_1071': 0, 'sign_2259': 0.4},
 'symptoms': {'symptom_12': 1,
 'symptom_135': 0.5,
 'symptom_34': 0,
 'symptom_40': -0.22229441461509403,
 'symptom_5': 0.20000000000000001,
 'symptom_96': 0}}
 ```

### Diagnostic API
 The diagnostic API resides at `localhost:8080/diagnose`.  It takes a git request with k:v arguments where the key is a sign or symptom and the value is the value of the sign or symptom.  once called, it returns a JSON list of diagnoses in priority order with relatives scores:
 ```
 {'diagnosis_2287': 0.03583184375312342,
'diagnosis_2497': 0.03916503852085583,
'diagnosis_2635': 0.86711857628206257,
...}
```
### Truth API
The truth API provides a means for identifying what the 'true' signs or symptoms associated with a diagnosis were in the truth data underlying the training data.  It may be found at `localhost:8080/truth` with argument `truth` with a value of the diagnosis to identify the truth signs and symptoms for.  It returns a JSON dictionary of the form:
```
{'diagnosis_6827': {'signs': {'sign_1534': {'factors': {'inverse': True},
 'function': 'bool',
'function_type': 'categorical'},
 'sign_1939': {'factors': {'inverse': True},
 'function': 'bool',
'function_type': 'categorical'},
 'sign_2345': {'factors': {'inverse': False},
 'function': 'bool',
'function_type': 'categorical'},
 'sign_59': {'factors': {'levels': [0.1,
 0.2,
0.3,
0.4,
...},
 'symptoms': {'symptom_112': {'factors': {'inverse': True},
 'function': 'bool',
'function_type': 'categorical'},
 'symptom_134': {'factors': {'inverse': True},
 'function': 'bool',
 'function_type': 'categorical'},
 'symptom_25': {'factors': {'levels': [1,
 0.5,
 -1]}
 ...}}}
 ```



