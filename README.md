
# Code for the Thesis work "Regional Transferability of Graph Neural Networks for Traffic Forecasting"

### Author: Ivans Kravcevs, Supervisor: Elena Congeduti

## Overview

This repository is based on the code for the DCRNN model - [pytorch-DCRNN](https://github.com/xlwang233/pytorch-DCRNN).

This repository contains the code developed for the thesis project on "Regional Transferability of Graph Neural Networks for Traffic Forecasting". The project explores the application of transferability techniques to improve the performance and generalizability of GNN models in traffic forecasting.

## Repository Structure

```
transferability_code/
│
├── graph_selection/ (Implementation of graph selection techniques)
│   ├── bucketed_simulated_annealing.py (File with the introduced BSA algoirthm for graph selection)
│   ├── distance_functions.py 
│   ├── random_graphs.py (Random graph selection)
│   ├── simulated_annealing.py (Implementation of SA algorithm)
│   ├── simulated_annealing_helper_functions.py
│   └── take_subset_dataset.py
│
├── lib/
│   └── ... (DCRNN code)
│
├── model/
│   └── ... (DCRNN code)
│
├── results/ (Result visualization code)
│   ├── plot_results.py
│   ├── plotting_sensor_predictions.py
│   └── take_error.py
│
├── runs/
│   └── ... (DCRNN code)
│
├── scripts/
│   └── ... (DCRNN code)
│
│
├──full_testing.py  (File to test the error of the selected graphs using the pre-trained model)
└── ...
```

## Acknowledgments

This project was developed as part of a bachelor thesis work at Delft University of Technology. Special acknowledgements to the project supervisor [Elena Congeduti](https://www.tudelft.nl/ewi/over-de-faculteit/afdelingen/intelligent-systems/interactive-intelligence/people/current-group-members/elena-congeduti) for guidance and support and my teammates 
Alex Păcurar	(*a.v.pacurar-1@student.tudelft.nl*), 
Vlad Vrânceanu	(*v.g.vranceanu@student.tudelft.nl*),	
Danae Savvidi	(*d.n.savvidi@student.tudelft.nl*),
Wiktor Grzybko	(*w.j.grzybko@student.tudelft.nl*)