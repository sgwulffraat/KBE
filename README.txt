This is an application to optimize the placement of EWIS connectors as commissioned by GKN Fokker Elmo.
The application is created by Cor Zoon and Stijn Wulffraat.
The user must possess a working parapy license in order for this application to work.

The user can use an existing bracket geometry as a STEP file as input or can generate a simple circular or rectangular bracket within the application.
After the bracket is either loaded in or specified, the connectors can be selected. Right now only a selection of 4 different connectors can be used as an input for the optimization but this can be extended on request in the future.
The available types of connectors are derived from an excel file supplied by GKN Fokker Elmo. After the desired type and corresponding number of connectors have been selected the optimization can be carried out.
The optimization is performed using an evolutionary algorithm designed by Albert Espin. The optimization quality of the solution using this algorithm is poor for a relative short number of iterations.
However, the optimization settings can be changed from within the parapy gui. Meaning that a coarse solution leading to small calculation times can be used in the initial design phase and a more refined solution can be obtained later in the design phase but with much longer running times.
The ADD SETTING HERE can be adjusted to find a multiple of solutions of which the most optimal is selected by the application.
The ADD SETTING HERE can be adjusted to increase or decrease to total number of iterations per solution.

The following packages must be installed:
Shapely 1.7.1 (newer verions result in errors)
pandas
numpy
pickle
Parapy
openpyxl