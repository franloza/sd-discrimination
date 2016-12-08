"""
Module that includes all the functions for Subgroup Discovery (SD)
"""
from enum import Enum
import logging

def sd(df):
    #Define quality measures
    QualityMeasure = Enum('Quality Measure', 'WRA Specificity Sensitivity')

    evaluate(QualityMeasure.WRA,df)


def evaluate(QualityMeasure,df):
    """Execute an evaluation function for a certain quality measure.""" 
    evaluator = {
        QualityMeasure.WRA: evaluate_wra,
        QualityMeasure.Specificity: evaluate_specificity,
        QualityMeasure.Sensitivity: evaluate_sensitivity,
    }
    return evaluator.get(QualityMeasure)(df)


def evaluate_wra (df):
    """Returns the Weighted Relative Accuracy of a group.""" 
    logging.debug('Evaluating Weighted Relative Accuracy')
    #TODO: Implement this function

def evaluate_specificity (df):
    """Returns the Specificity of a group.""" 
    logging.debug('Evaluating Specificity')
    #TODO: Implement this function

def evaluate_sensitivity (df):
    """Returns the Sensitivity of a group.""" 
    logging.debug('Evaluating Sensitivity')
    #TODO: Implement this function