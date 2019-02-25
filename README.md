# PerformanceEstimator
This is the python code (v3.7.2) to implement the Performance Estimation activitiy in PHANTOM project. 

Performance estimation estimates the non-functional properties (e.g., execution time, energy consumption) of newly designed applications by analyzing PHANTOM component network and previous non-functional testing results.
The input is the xml file of the "ComponentNetwork" of an application describing the inner components and their communications following PHANTOM specification, while the output is the estimation result to terminal and destination xml file. No external framework is needed to support the execution.

After downloading the code, the performance estimator can be run by using the following command, where [input_component_network] is the input component network with full name and path.

	python PerformanceEstimator.py [input_component_network]
	
The following two variables can be configured at the beginnig of the source code in PerformanceEstimator.py file:
	
	tested_component_results_file_path
	output_estimation_result_file_path
The "tested_component_results_file_path" indicates where the previous testing result file can be found to support the performance estimation, and the "output_estimation_result_file_path" indiciates the target file to store the performance estimation result. 

A

	
	
