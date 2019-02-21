#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# several instances of the same component in a component network file should have different component_name
# the component definition in a component network file is supposed to be ordered, which means that the first component to be executed the is at the top of the list, and the last componnet to be executed is at the bottom. In the case that one same component "A" is both the first and last component to be executed, the last communication object in the component network definition should target the component "A"

import sys
import Component, Graph
from Component import TestedComponent, PerformanceMetrics, InputComponent, COMM
from Graph import NetworkGraph
from xml.dom import minidom
import xml.etree.ElementTree as ET

tested_component_results_file_path = "D:\Code\Python\PerformanceEstimator_v1\TestedComponents.xml"
output_estimation_result_file_path = "D:\Code\Python\PerformanceEstimator_v1\EstimationResult.xml"
component_network_all_tested = True

#read python input parameters
#print ('Number of arguments:', len(sys.argv), 'arguments.')
if len(sys.argv) == 1:
    print('A component network file is missing as an input')
elif len(sys.argv) == 2:
    #py PerformanceEstimator.py D:\Code\Python\PerformanceEstimator_v1\Component-Network.xml
    component_network_path = sys.argv[1]
    print(component_network_path)
elif len(sys.argv) >= 3:
    print("Hi, you are reaching the end of the world; this is an advanced option for further exploitation")
else:
    pass

if len(sys.argv) == 1:
    component_network_path = 'D:\Code\Python\PerformanceEstimator_v1\Component-Network.xml'
else:
    pass

print("- 1. Analyzing Input of Component Network -")
#read the file of tested components
tested_components_file = open(tested_component_results_file_path)
tested_components_str = tested_components_file.read()
tested_components_file.close()

#deserilize file elements to tested component objects
tested_components_xml = minidom.parseString(tested_components_str)
tested_components_elements = tested_components_xml.getElementsByTagName("TestedComponent")
tested_components = []
for tested_component_element in tested_components_elements:
    pm_list = []
    i = 0
    for index in tested_component_element.childNodes:
        if(i % 2) == 1:
            pm = PerformanceMetrics(index.attributes["hardware"].value, float(index.attributes["execution_time"].value), float(index.attributes["energy_consumption"].value), float(index.attributes["ram_usage"].value))
            pm_list.append(pm)
        i=i+1
    tested_component = TestedComponent(tested_component_element.attributes["application_name"].value, tested_component_element.attributes["component_name"].value, pm_list)
    tested_components.append(tested_component)

#read input file of component network
component_network_file = open(component_network_path)
component_network_str = component_network_file.read()
component_network_file.close()

#deserilize file elements to input_components and input_comms
input_components = []
input_comms = []
component_network_xml = minidom.parseString(component_network_str)

component_network_application_name = ""
try:
    application_name_xml = component_network_xml.getElementsByTagName("application")
    component_network_application_name = application_name_xml.item(0).attributes["name"].value
except (RuntimeError, TypeError, NameError):
    pass

components_elements = component_network_xml.getElementsByTagName("component")
for component_element in components_elements:
    component_name = component_element.attributes["name"].value
    input_component = InputComponent(component_network_application_name, component_name)
    input_components.append(input_component)
#start_component is by defaut the first component defined in the component network file, while the end_component is the last component defined
#in case that start_component and the end_component is the same component to read input files and generate output files, the end_component is updated in the next block
start_component = input_components[0]
end_component = input_components[len(input_components)-1]

comm_elements = component_network_xml.getElementsByTagName("comm-object")
for comm_element in comm_elements:
    comm_name = comm_element.attributes["name"].value
    source_xml = comm_element.getElementsByTagName("source")
    target_xml = comm_element.getElementsByTagName("target")
    source_name = source_xml.item(0).attributes["name"].value
    target_name = target_xml.item(0).attributes["name"].value
    comm = COMM(comm_name, source_name, target_name)
    input_comms.append(comm)
if input_comms[len(input_comms)-1].target == start_component.component_name:
    end_component = start_component

print("- 2. Searching Previously Testing Results -")
#check if all input_componnets are previously tested, if yes, set component_network_all_tested = True
for input_component in input_components:
    input_component_tested = False
    for tested_component in tested_components:
        if input_component.component_name == tested_component.component_name:
            input_component_tested = True
    if input_component_tested == False:
        component_network_all_tested = False
        break
#stop the program, if the input component network contains untested component
if (component_network_all_tested == False):
    sys.exit("The input component network contains untested component")

# search the optimal performance metrics for each input_component, the input_component only contain the optimal performance metrics and pm associated hardware
for input_component in input_components:
    for tested_component in tested_components:
        if input_component.component_name == tested_component.component_name:
            input_component.pm = tested_component.pm_list[0]
            i = 0
            for pm in tested_component.pm_list:
                if tested_component.pm_list[i].execution_time < input_component.pm.execution_time:
                    input_component.pm = tested_component.pm_list[i]
                i = i + 1
        else:
            pass

print("- 3. Estimating the Performance Metrics of Input Component Network -")
#always use the path with the worst results as the estimation results, and this is valide for PHANTOM because only sequence and parallel execution patterns are included in the component network

"""
# test store/printAllPaths and store/printAllPaths2
vertices = [0, 1, 2, 3]
g = NetworkGraph(vertices)
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(0, 3)
g.addEdge(2, 0)
g.addEdge(2, 1)
g.addEdge(1, 3)
s = 2
e = 2
step = 0
visited = {0:False, 1:False, 2:False, 3:False}
path = []
paths = []
g.storeAllPaths(s, e, step, visited, path, paths)
"""

#transform input components and comms into a graph
input_component_network = NetworkGraph(input_components)
source_updated = False
target_updated = False
for input_comm in input_comms:
    for input_component in input_components:
        if input_component.component_name == input_comm.source:
            source_component = input_component
            source_updated = True
        if input_component.component_name == input_comm.target:
            target_component = input_component
            target_updated = True
    #if don't exist, then add;
    if source_updated == True and target_updated == True:
        input_component_network.addEdge(source_component, target_component)
    source_updated = False
    target_updated = False
"""
for key in input_component_network.graph.keys():
    print(key, key.component_name, input_component_network.graph[key])
for input_component in input_components:
    print(input_component, input_component.component_name)
"""

#search all paths from start_component to end_component, and store them in paths
step  = 0
visited = {}
for input_component in input_components:
    visited[input_component] = False
path = []
paths = [] #here stores a deep copy of relevant component information
input_component_network.storeAllPaths(start_component, end_component, step, visited, path, paths)

#calculate the aggregated value of each path's performance metrics, and store them in path_pm_list[]
path_aggregated_pm_list = []
for path in paths:
    aggregated_pm = PerformanceMetrics("default", 0.0, 0.0, 0.0)
    for component in path:
        aggregated_pm.execution_time = aggregated_pm.execution_time + component.pm.execution_time
        aggregated_pm.energy_consumption = aggregated_pm.energy_consumption + component.pm.energy_consumption
        aggregated_pm.ram_usage = aggregated_pm.ram_usage + component.pm.ram_usage
    path_aggregated_pm_list.append(aggregated_pm)
#for aggregated_pm in path_aggregated_pm_list:
#    print(aggregated_pm.execution_time,aggregated_pm.energy_consumption, aggregated_pm.ram_usage)

#calculate the final results for three estimation properties
total_execution_time = 0
total_energy_consumption = 0
total_ram_usage = 0
for aggregated_pm in path_aggregated_pm_list:
    if aggregated_pm.execution_time > total_execution_time:
        total_execution_time = aggregated_pm.execution_time
    total_energy_consumption = total_energy_consumption + aggregated_pm.energy_consumption
    total_ram_usage = total_ram_usage + aggregated_pm.ram_usage

print("- 4. The Estimation Results are below -")
print("Estimated Execution Time:    ", total_execution_time, "ns")
print("Estimated Energy Consumption:", total_energy_consumption)
print("Estimated Ram Usage:         ", total_ram_usage)
print("The complete result can be found in: '%s'" %(output_estimation_result_file_path))

performance_estimation_xml = ET.Element('PerformanceEstimation')
performance_estimation_xml.set('application_name', component_network_application_name)
estimation_result_xml = ET.SubElement(performance_estimation_xml, 'EstimationResult')
estimation_result_xml.set("execution_time", str(total_execution_time))
estimation_result_xml.set("energy_consumption", str(total_energy_consumption))
estimation_result_xml.set("ram_usage", str(total_ram_usage))
reference_mapping_xml = ET.SubElement(performance_estimation_xml, 'ReferenceMapping')
for input_component in input_components:
    input_component.addToXML(reference_mapping_xml)

xml_as_string = ET.tostring(performance_estimation_xml, encoding="unicode",method="xml")
tmp = minidom.parseString(xml_as_string)
pretty_xml_as_string = tmp.toprettyxml()

myfile = open(output_estimation_result_file_path, "w")
myfile.write(pretty_xml_as_string)
myfile.close()


