# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# Filename: Component.py
import xml.etree.ElementTree as ET

class PerformanceMetrics:
    hardware = "default"
    execution_time = 0.0
    energy_consumption = 0.0
    ram_usage = 0.0
    def __init__(self):
        pass
    def __init__(self, hw, et, ec, ru):
        self.hardware = hw
        self.execution_time=et
        self.energy_consumption=ec
        self.ram_usage=ru

class TestedComponent:
    application_name = ""
    component_name = ""
    pm_list = []
    def __init__(self, an, cn, input_pm_list):
        self.application_name=an
        self.component_name=cn
        self.pm_list = []
        for input_pm in input_pm_list:
            self.pm_list.append(input_pm)
    def addToPMlist(self,pm):
        self.pm_list.append(pm)
    def addToXML(self, testedComponents):    #add this tested component profile to the element tree for XML serialization
        tc = ET.SubElement(testedComponents, 'TestedComponent')
        tc.set('application_name',self.application_name)
        tc.set('component_name',self.component_name)
        for pm_element in self.pm_list:
            pm = ET.SubElement(tc, 'PerformanceMetric')
            pm.set('hardware', pm_element.hardware)
            pm.set('execution_time', str(pm_element.execution_time))
            pm.set('energy_consumption', str(pm_element.energy_consumption))
            pm.set('ram_usage', str(pm_element.ram_usage))

class InputComponent:
    application_name = ""
    component_name = ""
    # the input component only reads and stores the optimal performance metrics among the list
    pm = PerformanceMetrics("default", 0.0, 0.0, 0.0)
    def __init__(self, an, cn):
        self.application_name = an
        self.component_name = cn
    def addToXML(self, reference_mapping_xml):    #add the input component to reference mapping for xml serialization
        tc = ET.SubElement(reference_mapping_xml, 'EstimationResult')
        tc.set('component_name',self.component_name)
        tc.set('target_hardware',self.pm.hardware)

class COMM: #communication object
    name = ""
    source = ""
    target = ""
    def __init__(self, n, s, t):
        self.name = n
        self.source = s
        self.target = t

class Path:
    path_components = []
    def __init__(self, path_components):
        self.path_components.copy(path_components)
