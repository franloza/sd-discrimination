"""
Module that includes all the functions for Subgroup Discovery (SD)
"""
import logging
import math
from enum import Enum

def sd(dataset):
    """
    Main function for subgroup discovery. Configure the subgroup to evaluate it
    """

    ####################### CONFIGURE THIS ##############################

    #Create subgroup
    #You can include as many conditions as you want (2 conditions is OK for interpretability)
    
    #Example
    #subgroup = dataset[(dataset['race'] == 'Latino/Hispanic American') & (dataset['age'] > 23)]

    subgroup = dataset[(dataset['like'] >= 7.0)]

    #####################################################################

    logging.info("Subgroup discovery")

    #Define quality measures
    QualityMeasure = Enum('Quality Measure', 'WRA Specificity Sensitivity ChiSquare')

    lengthDataset = len(dataset)
    logging.debug('Examples of the dataset {}'.format(lengthDataset))  
    logging.debug('Examples of subgroup: {} ({:.2f}%)'.format(len(subgroup), len(subgroup)/lengthDataset))
    
    evaluate(QualityMeasure.WRA,dataset,subgroup,'match')
    evaluate(QualityMeasure.Specificity,dataset,subgroup,'match')
    evaluate(QualityMeasure.Sensitivity,dataset,subgroup,'match')
    evaluate(QualityMeasure.ChiSquare,dataset,subgroup,'match')


def evaluate(QualityMeasure,dataset,subgroup,targetColumn):
    """Execute an evaluation function for a certain quality measure.""" 
    evaluator = {
        QualityMeasure.WRA: evaluate_wra,
        QualityMeasure.Specificity: evaluate_specificity,
        QualityMeasure.Sensitivity: evaluate_sensitivity,
        QualityMeasure.ChiSquare: evaluate_chi_square,
    }
    return evaluator.get(QualityMeasure)(dataset,subgroup,targetColumn)


def evaluate_wra (dataset,subgroup,targetColumn):
    """Returns the Weighted Relative Accuracy of a subgroup."""   
    #Get confusion matrix
    cf = confusion_matrix(dataset,subgroup,targetColumn)
    
    #Calculate Weighed Relative Accuracy
    WRAcc = cf[0][0] - (cf[0][0] + cf[0][1]) * (cf[0][0] + cf[1][0])
    logging.info('WRAcc: {:.6f}'.format(WRAcc))
    return WRAcc

def evaluate_specificity (dataset,subgroup,targetColumn):
    """Returns the Specificity of a subgroup."""    
    #Get confusion matrix
    cf = confusion_matrix(dataset,subgroup,targetColumn)
    
    #Calculate specificity
    specificity = 1 - (cf[1][0] / (cf[1][0] + cf[1][1]))
    logging.info('Specificity: {:.6f}'.format(specificity))
    return specificity

def evaluate_sensitivity (dataset,subgroup,targetColumn):
    """Returns the Sensitivity of a subgroup."""
    #Get confusion matrix
    cf = confusion_matrix(dataset,subgroup,targetColumn)
    
    #Calculate sensitivity
    sensitivity = cf[0][0] / (cf[0][0] + cf [0][1])
    logging.info('Sensitivity: {:.6f}'.format(sensitivity))
    return sensitivity

def evaluate_chi_square (dataset,subgroup,targetColumn):
    """Returns the Chi Square statistic of a subgroup.""" 
    #Get confusion matrix
    cf = confusion_matrix(dataset,subgroup,targetColumn)
    P = cf[0][0] + cf [0][1]
    N = cf[1][0] + cf [1][1]

    #Calculate chi square
    chi_square = (P + N) * (correlation (cf) ** 2)
    logging.info('Chi Square: {:.6f}'.format(chi_square))
    return chi_square

def correlation (cf):
    """Returns the correlation metric given a confusion matrix."""
    p = cf[0][0]
    n = cf[0][1]
    P = p + cf[0][1]
    N = n + cf[1][1]
    return (p*N - P*n) / math.sqrt(P*N*(p+n)*(P-p+N-n))

def confusion_matrix (dataset,subgroup,targetColumn):
    """Returns the confusion matrix of a dataset with a subgroup.""" 
    total_rows = len(dataset)

    #Calculate the complement of the dataset over the subgroup
    complement = dataset[~dataset.index.isin(subgroup.index)]

    #Elements of confusion matrix
    subgroup_pos_target_rate = len(subgroup[subgroup[targetColumn] == 1]) / total_rows
    subgroup_neg_target_rate = len(subgroup[subgroup[targetColumn] == 0]) / total_rows
    complement_pos_target_rate = len(complement[complement[targetColumn] == 1]) / total_rows
    complement_neg_target_rate = len(complement[complement[targetColumn] == 0]) / total_rows
    
    return [[subgroup_pos_target_rate,complement_pos_target_rate],
            [subgroup_neg_target_rate,complement_neg_target_rate]]


def sd_beamSearch(dataset):
    target = 'match'
    width = 10
    depth = 3
    bins = 3
    subgroups = [(set(), dataset, 0)]
    descriptors = []

    for column in dataset.columns:
        if (dataset[column].dtype == "float64" or dataset[column].dtype == "int64"):
            descriptors.append((column, getDescriptorsEW(dataset, column, bins)))
    #logging.debug(descriptors)
    for level in range(depth):
        logging.debug("level " + str(level))
        newsubgroups = []
        for subgroup in subgroups:
            print(subgroup[0])
            for descriptor in descriptors:
                if not ((descriptor[0] == target) or (descriptor[0] in subgroup[0])):
                    columns = subgroup[0] | set([descriptor[0]])
                    for subbin in descriptor[1]:
                        bin = subgroup[1][subbin]
                        val = evaluate_wra(dataset, bin, target)
                        newsubgroup = (columns, bin, val)
                        newsubgroups.append(newsubgroup)
        subgroups = []
        newsubgroups.sort(reverse=True,key=lambda x: x[2])
        seen = set()
        for sg in newsubgroups:
            if (str(sg[0]) not in seen):
                subgroups.append(sg)
                seen.add(str(sorted(sg[0])))
        print(len(newsubgroups))
        subgroups = subgroups[:width]
        for sg in subgroups:
            print(sg[0], sg[2])




def getDescriptorsEW (dataset, column, bins):
    width = (max(dataset[column]) - min(dataset[column]))/bins
    logging.debug("column=" + str(column) + ", width=" + str(width))
    descriptors = []
    start = min(dataset[column]) - 1
    for x in range(bins):
        end = min(dataset[column]) + (x+1 * width)
        bin = (dataset[column] > start) & (dataset[column] <= end)
        #print(start, end)
        #print(bin.value_counts())
        descriptors.append(bin)
        start = end
    return descriptors
