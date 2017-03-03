# General code for analysis of the validation results

import json
import pandas as pd
import matplotlib as plt
import numpy as np

RESULTS_FILE = "/Users/v685573/OneDrive/Documents/MSIA5243/practicum/results.json"
PLOT_STYLES  = [".", "o", "v", "^", ">", "<", "*", "h", "+", "x", "D"]
NUM_TRAIN_RECORDS = [100000, 200000, 400000, 600000, 800000, 1000000, 1300000, 1600000, 2500000, 3200000, 5000000]


with open(RESULTS_FILE, 'r') as f:
    results = json.load(f)

# PLot data ontop of itself
for i in range(len(results)):
    plt.plot(results[str(NUM_TRAIN_RECORDS[i])]['locs'], results[str(NUM_TRAIN_RECORDS[i])]['scores'], PLOT_STYLES[i])


# top scores

top = np.array([[0,0,0]])
for k, v in results.iteritems():
    top = np.append(top, [[int(k), v['top'], v['top5']]], axis=0)
top = pd.DataFrame(top, columns=['Training Records', 'Top', 'Top5'])
top.sort(columns='Training Records', ascending=False, inplace=True)
top.reset_index(drop=True, inplace=True)
f = figure()
plot(top['Training Records'], top['Top'], '-D', label='Top Diagnosis', color='black')
plot(top['Training Records'], top['Top5'], '-x', label="In Top 5", color='black')
legend(loc=4)
xlabel('Number of Training Records Used')
ylabel('Correct Diagnoses out of 1000')
title('Model Success at Various Training Levels')
f.patch.set_facecolor('white')


# plot separate plots. scatter
f, plots = plt.subplots(3, 4)
for p in range(len(NUM_TRAIN_RECORDS)):
    y = p%4
    x = p/4
    print x, y
    plots[x][y].plot(results[str(NUM_TRAIN_RECORDS[p])]['locs'], results[str(NUM_TRAIN_RECORDS[p])]['scores'], 'x', color='black')
    plots[x][y].set_title(NUM_TRAIN_RECORDS[p])
# figure title
f.suptitle("Score Difference from Top Diagnosis vs Location of Correct Diagnosis")
# y label
f.text(.05, .55, "Score Difference", rotation='vertical')
# x label
f.text(.42, .05, "Location In Sorted List of Diagnoses", va='center')
# set the background color to white
f.patch.set_facecolor('white')



# Plot locs
f, plots = plt.subplots(3, 4)
for p in range(len(NUM_TRAIN_RECORDS)):
    y = p%4
    x = p/4
    #print x, y
    plots[x][y].hist(results[str(NUM_TRAIN_RECORDS[p])]['locs'], color='black')
    plots[x][y].set_title(NUM_TRAIN_RECORDS[p])
# figure title
f.suptitle("Position of Correct Diagnosis in List Ordered by Scores")
# y label
f.text(.05, .6, "Number of Correct Diagnoses in Bin", rotation='vertical')
# x label
f.text(.4, .05, "Location in List of Diagnoses Sorted by Score", va='center')
# set the background color to white
f.patch.set_facecolor('white')

# Plot locs (limited)
num_records_two = NUM_TRAIN_RECORDS[2:]
f, plots = plt.subplots(3, 3)
for p in range(len(num_records_two)):
    y = p%3
    x = p/3
    #print x, y
    plots[x][y].hist(results[str(num_records_two[p])]['locs'], color='black', range=[0, 60])
    plots[x][y].set_title(num_records_two[p])
# figure title
f.suptitle("Position of Correct Diagnosis in List Ordered by Scores")
# y label
f.text(.05, .6, "Number of Correct Diagnoses in Bin", rotation='vertical')
# x label
f.text(.4, .05, "Location in List of Diagnoses Sorted by Score", va='center')
# set the background color to white
f.patch.set_facecolor('white')



# Plot scores
f, plots = plt.subplots(3, 4)
for p in range(len(NUM_TRAIN_RECORDS)):
    y = p%4
    x = p/4
    print x, y
    plots[x][y].hist(results[str(NUM_TRAIN_RECORDS[p])]['scores'], color='black')
    plots[x][y].set_title(NUM_TRAIN_RECORDS[p])
# figure title
f.suptitle("Percent Difference of Correct Diagnosis from Top Scoring Diagnosis")
# y label
f.text(.05, .55, "Number of Diagnoses in Bin", rotation='vertical')
# x label
f.text(.45, .05, "Difference in Score", va='center')
# set the background color to white
f.patch.set_facecolor('white')

# list top-10 counts
for p in range(len(NUM_TRAIN_RECORDS)):
    print NUM_TRAIN_RECORDS[p], len([x for x in results[str(NUM_TRAIN_RECORDS[p])]['locs'] if x <= 10 and x > -1])

# Degree distributions
GIT_DIR = "/Users/v685573/OneDrive/Documents/MSIA5243/code/practicum"
NUM_TRAIN_RECORDS = 1000000  # Number of records to use in training the model.  I'd recommend 100-1000 times the number of diagnoses
NUM_TEST_RECORDS = 10000  # Number of records to use to use in testing the model
MODELS = 5  # Number of times to add NUM_TRAIN_RECORDS to the data.records set and recreate the model.
import imp
# Generate Synthetic Data
print "Loading the synthetic data generation module."
fp, pathname, description = imp.find_module("synthetic", [GIT_DIR])
synthetic = imp.load_module("synthetic", fp, pathname, description)
# Create class instance
print "Creating the synthetic data object 'data' and truth data."
data = synthetic.test_data()

data.records = list()
degree_dists = dict()
for i in range(1,MODELS):
    # Create records
    print "Creating the synthetic noisy records."
    data.records = data.records + data.create_diagnosis_data(data.truth, NUM_TRAIN_RECORDS, data.default)


    # Train a model based on the synthetic data
    print "Loading the model module."
    fp, pathname, description = imp.find_module("model", [GIT_DIR])
    model = imp.load_module("model", fp, pathname, description)
    # Create decision support system object
    print "Creating the medical decision support system object 'mdss'."
    mdss = model.decision_support_system()
    print "Creating the model."
    mdss.model = mdss.train_nx_model(data.records)

    # Get all pairings
    edges = set()
    for edge in mdss.records_graph.edges_iter():
        edges.add(edge)
    
    deg = list()
    # Get all counts per pairing
    for edge in edges:
        deg.append(len(mdss.records_graph.edge[edge[0]][edge[1]]))

    degree_dists[len(data.records)] = deg

keys = sorted(degree_dists.keys())

f, plots = plt.subplots(2, 3)
for p in range(len(keys)):
    y = p%3
    x = p/3
    print x, y
    plots[x][y].hist(degree_dists[keys[p]], color='black')
    plots[x][y].set_title(keys[p])
# figure title
f.suptitle("Relationship Count between Signs/Symptoms and Diagnoses")
# y label
f.text(.05, .55, "Relationship Tuples in Bin", rotation='vertical')
# x label
f.text(.42, .05, "Number of Relationships for Tuple", va='center')
# set the background color to white
f.patch.set_facecolor('white')





# TODO:  Plot quartiles of locations (67, 97, 99)