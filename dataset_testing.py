import csv
import numpy as np
fr = []
Er = 4.4
h_mm = 1.6
W_mm = [] 
L_mm = []  
Leff_mm = [] 
dL_mm = []
eps_eff = []
g1_S = []
g12_S = []
Rin_edge_ohm = []
Feed_W_mm = []
Feed_L_mm= []
Ground_L_mm= []
Ground_W_mm= []
RadBox_L_mm = 0
RadBox_W_mm = 0 
RadBox_H_mm = 0

with open('antenna_dataset_Gs_full.csv', 'r') as file :
    csvreader = csv.reader(file)
    next(csvreader)

    for line in csvreader :
        fr.append(line[1])
        W_mm.append(line[4])
        L_mm.append(line[5])
        #Leff_mm.append(line[6])
        #dL_mm.append(line[7])
        #eps_eff.append(line[8])
        #g1_S.append(line[9])
        #g12_S.append(line[10])
        #Rin_edge_ohm.append(line[11])
        Feed_W_mm.append(line[12])
        #Feed_L_mm.append(line[13])
        Ground_L_mm.append(line[14])
        Ground_W_mm.append(line[15])
        
    print(len(file))
    for i in range(1, len(line)):
        print(fr[i], " , ", W_mm[i]," , ", L_mm[i],"\n")
    
        