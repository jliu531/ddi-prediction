'''
Jason L

This script creates six csv files based on the 2013 DDI Corpus and was developed in Python 3.6.

The corpus is available at http://labda.inf.uc3m.es/doku.php?id=en:labda_downloadddicorpus

We thank Isabel Segura-Bedmar for the creation of the DDI Corpus. 

Relevant References:
María Herrero-Zazo, Isabel Segura-Bedmar, Paloma Martínez, Thierry Declerck, The DDI corpus: An annotated corpus with pharmacological substances and drug–drug interactions, Journal of Biomedical Informatics, Volume 46, Issue 5, October 2013, Pages 914-920, http://dx.doi.org/10.1016/j.jbi.2013.07.011.

Isabel Segura-Bedmar, Paloma Martínez, María Herrero Zazo, (2014). Lessons learnt from the DDIExtraction-2013 shared task, Journal of Biomedical Informatics, Vol.51, pp:152-164.

Files created:

-A train (named_entity_set_train.csv) and test (named_entity_set_test.csv) set containing the sentence_id, text, position, entity, and entity_type in the columns

-A train (ddi_train_grouped_sentences.csv) and test (ddi_test_grouped_sentences.csv) set containig information on whether or not if ANY drug pair in the sentence describes a drug drug interaction. Only the first true or false instance of a drug-drug interation is used. Columns include:
    --sentence_id
    --text
    --ddi_type

-A train (ddi_train.csv) and test (ddi_test.csv) set cointaing all information about drug-drug interaction pairs. Columns include:
    --sentence_id
    --text
    --pair_id
    --entity1_id
    --entity1_name
    --entity1_type
    --entity2_id
    --entity2_name
    --entity2_type
    --ddi_exists
    --ddi_type
'''

import xml.etree.ElementTree as ET
import csv
import os

path = '.\APIforDDICorpus\DDICorpus\Train\DrugBank'
path_medline = '.\APIforDDICorpus\DDICorpus\Train\MedLine'
paths = [path, path_medline]

#create training set for named entity recognition and dictionary with entity id as the key and a list containing
#the drug name and type as the value
file = open('named_entity_set_train.csv', 'w')
writer = csv.writer(file, lineterminator = '\n')
entity_dict_train = {}

for path in paths:
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            tree = ET.parse(f'{path}\\{filename}')

        #parse xml
        lines = []
        for sentence in tree.getroot().findall('sentence'):
            sentence_id = sentence.attrib.get('id')
            sentence_text = sentence.attrib.get('text').lower()
            for entity in sentence.findall('entity'):
                location = entity.attrib.get('charOffset')
                entity_name = entity.attrib.get('text').lower()
                entity_type = entity.attrib.get('type').lower()
                entity_id = entity.attrib.get('id')
                if entity_dict_train.get(entity_id, 0) == 0:
                    entity_dict_train[entity_id] = [entity_name, entity_type]
                row = [sentence_id, sentence_text, location, entity_name, entity_type]
                lines.append(row)

        #add to csv file
        writer.writerows(lines)

file.close()

file = open('ddi_train.csv', 'w')
writer = csv.writer(file, lineterminator = '\n')
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            tree = ET.parse(f'{path}\\{filename}')
    
        #parse xml
        lines = []
        for sentence in tree.getroot().findall('sentence'):
            if sentence.find('pair') is not None:
                sentence_id = sentence.attrib.get('id')
                sentence_text = sentence.attrib.get('text').lower()
                for pair in sentence.findall('pair'):
                    pair_id = pair.attrib.get('id')
                    e1_id = pair.attrib.get('e1')
                    e1_name = entity_dict_train[e1_id][0]
                    e1_type = entity_dict_train[e1_id][1]
                    e2_id = pair.attrib.get('e2')
                    e2_name = entity_dict_train[e2_id][0]
                    e2_type = entity_dict_train[e2_id][1]
                    ddi = pair.attrib.get('ddi')
                    ddi_type = None if pair.attrib.get('type') is None else pair.attrib.get('type')
                    row = [sentence_id, sentence_text, pair_id, e1_id, e1_name, e1_type, e2_id, e2_name, e2_type, ddi, ddi_type]
                    lines.append(row)

        #add to csv file
        writer.writerows(lines)

file.close()

file = open('ddi_train_grouped_sentences.csv', 'w')
writer = csv.writer(file, lineterminator = '\n')
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            tree = ET.parse(f'{path}\\{filename}')
    
        #parse xml
        lines = []
        for sentence in tree.getroot().findall('sentence'):
            if sentence.find('pair') is not None:
                sentence_id = sentence.attrib.get('id')
                sentence_text = sentence.attrib.get('text').lower()
                pair_stored = 0 #flag to identify that at least one pair was recorded
                for pair in sentence.findall('pair'):
                    
                    #ddi pairs with attribute true aren't being recorded for some reason, fix bug
                    if pair.attrib.get('ddi') == 'false' and pair_stored == 0:
                        ddi = pair.attrib.get('ddi')
                        pair_stored = 1
                        row = [sentence_id, sentence_text, ddi]
                    if pair.attrib.get('ddi') == 'true':
                        ddi = pair.attrib.get('type')
                        row = [sentence_id, sentence_text, ddi]
                        break
                lines.append(row)
                    
                        

        #add to csv file
        writer.writerows(lines)

file.close()

path_drugbank_test = '.\APIforDDICorpus\DDICorpus\Test\Test for DrugNER task\DrugBank'
path_medline_test = '.\APIforDDICorpus\DDICorpus\Test\Test for DrugNER task\MedLine'

#create test set for named entity recognition and dictionary with entity id as the key and a list containing
#the drug name and type as the value
file = open('named_entity_set_test.csv', 'w')
writer = csv.writer(file, lineterminator = '\n')
paths = [path_drugbank_test, path_medline_test]

for path in paths:
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            tree = ET.parse(f'{path}\\{filename}')

        #parse xml
        lines = []
        for sentence in tree.getroot().findall('sentence'):
            sentence_id = sentence.attrib.get('id')
            sentence_text = sentence.attrib.get('text').lower()
            for entity in sentence.findall('entity'):
                location = entity.attrib.get('charOffset')
                entity_name = entity.attrib.get('text').lower()
                entity_type = entity.attrib.get('type').lower()
                entity_id = entity.attrib.get('id')
                row = [sentence_id, sentence_text, location, entity_name, entity_type]
                lines.append(row)

        #add to csv file
        writer.writerows(lines)

file.close()

path_drugbank_test = '.\APIforDDICorpus\DDICorpus\Test\Test for DDI Extraction task\DrugBank'
path_medline_test = '.\APIforDDICorpus\DDICorpus\Test\Test for DDI Extraction task\MedLine'

file = open('ddi_test.csv', 'w')
writer = csv.writer(file, lineterminator = '\n')
paths = [path_drugbank_test, path_medline_test]
entity_dict_test = {}
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            tree = ET.parse(f'{path}\\{filename}')
    
        #parse xml
        lines = []
        for sentence in tree.getroot().findall('sentence'):
            if sentence.find('pair') is not None:
                sentence_id = sentence.attrib.get('id')
                sentence_text = sentence.attrib.get('text').lower()
                
                for entity in sentence.findall('entity'):
                    entity_id = entity.attrib.get('id')
                    entity_name = entity.attrib.get('text')
                    entity_type = entity.attrib.get('type')
                    if entity_dict_test.get(entity_id, 0) == 0:
                        entity_dict_test[entity_id] = [entity_name, entity_type]
                
                for pair in sentence.findall('pair'):
                    pair_id = pair.attrib.get('id')
                    e1_id = pair.attrib.get('e1')
                    e1_name = entity_dict_test[e1_id][0]
                    e1_type = entity_dict_test[e1_id][1]
                    e2_id = pair.attrib.get('e2')
                    e2_name = entity_dict_test[e2_id][0]
                    e2_type = entity_dict_test[e2_id][1]
                    ddi = pair.attrib.get('ddi')
                    ddi_type = None if pair.attrib.get('type') is None else pair.attrib.get('type')
                    row = [sentence_id, sentence_text, pair_id, e1_id, e1_name, e1_type, e2_id, e2_name, e2_type, ddi, ddi_type]
                    lines.append(row)

        #add to csv file
        writer.writerows(lines)

file.close()

file = open('ddi_test_grouped_sentences.csv', 'w')
writer = csv.writer(file, lineterminator = '\n')
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            tree = ET.parse(f'{path}\\{filename}')
    
        #parse xml
        lines = []
        for sentence in tree.getroot().findall('sentence'):
            if sentence.find('pair') is not None:
                sentence_id = sentence.attrib.get('id')
                sentence_text = sentence.attrib.get('text').lower()
                pair_stored = 0 #flag to identify that at least one pair was recorded
                for pair in sentence.findall('pair'):
                    
                    #ddi pairs with attribute true aren't being recorded for some reason, fix bug
                    if pair.attrib.get('ddi') == 'false' and pair_stored == 0:
                        ddi = pair.attrib.get('ddi')
                        pair_stored = 1
                        row = [sentence_id, sentence_text, ddi]
                    if pair.attrib.get('ddi') == 'true':
                        ddi = pair.attrib.get('type')
                        row = [sentence_id, sentence_text, ddi]
                        break
                lines.append(row)
                    
                        

        #add to csv file
        writer.writerows(lines)

file.close()














