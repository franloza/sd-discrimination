"""
Module that includes all the functions for Subgroup Discovery (SD)
"""
from enum import Enum
import logging

def sd(dataset):
    #Define quality measures
    QualityMeasure = Enum('Quality Measure', 'WRA Specificity Sensitivity')

    #Create subgroup
    subgroup = dataset[(dataset['race'] == 'Latino/Hispanic American') &
    (dataset['age'] > 23)]

    evaluate(QualityMeasure.WRA,dataset,subgroup,'match')


def evaluate(QualityMeasure,dataset,subgroup,targetColumn):
    """Execute an evaluation function for a certain quality measure.""" 
    evaluator = {
        QualityMeasure.WRA: evaluate_wra,
        QualityMeasure.Specificity: evaluate_specificity,
        QualityMeasure.Sensitivity: evaluate_sensitivity,
    }
    return evaluator.get(QualityMeasure)(dataset,subgroup,targetColumn)


def evaluate_wra (dataset,subgroup,targetColumn):
    """Returns the Weighted Relative Accuracy of a group.""" 
    logging.debug('Evaluating Weighted Relative Accuracy')
    total_rows = len(dataset)

    #Calculate the complement of the dataset over the subgroup
    complement = dataset[~dataset.index.isin(subgroup.index)]

    #Elements of confusion matrix
    subgroup_pos_target_rate = len(subgroup[subgroup[targetColumn] == 1]) / total_rows
    subgroup_neg_target_rate = len(subgroup[subgroup[targetColumn] == 0]) / total_rows
    complement_pos_target_rate = len(complement[complement[targetColumn] == 1]) / total_rows
    #complement_neg_target_rate = len(complement[complement[targetColumn] == 0]) / total_rows
    
    #Calculate Weighed Relative Accuracy
    WRAcc = subgroup_pos_target_rate - (subgroup_pos_target_rate +
    complement_pos_target_rate) * (subgroup_pos_target_rate + subgroup_neg_target_rate)
    logging.debug('WRAcc: {:4f}'.format(WRAcc))
    
    return WRAcc

def evaluate_specificity (dataset,subgroup,targetColumn):
    """Returns the Specificity of a group.""" 
    logging.debug('Evaluating Specificity')
    #TODO: Implement this function

def evaluate_sensitivity (dataset,subgroup):
    """Returns the Sensitivity of a group.""" 
    logging.debug('Evaluating Sensitivity')
    #TODO: Implement this function
    