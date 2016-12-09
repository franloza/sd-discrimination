"""
Module that includes all the commong functions for discrimination detection
"""
import logging
import pandas as pd

def discrimination(dataset):

    ####################### CONFIGURE THIS ##############################

    #Create subgroup A (Containing sensitive information)
    #subgroupA = dataset[(dataset['gender'] == 'female')]
    subgroupA = dataset[(dataset['race'] == 'Latino/Hispanic American')]

    #Create subgroup B (Containing predictive information)
    subgroupB = dataset[(dataset['interests_correlate'] > 0)]

    #####################################################################


    logging.info("Discrimination detection")

    #Create subgroup C (Label)
    subgroupC = dataset[dataset['match'] == 1]

    elift(dataset,subgroupA,subgroupB,subgroupC)


def elift (dataset, subgroupA, subgroupB, subgroupC):
    """
    Returns the elift measure of the subgroup AB with respect to a label (C)
    """

    #Get subgroup A,B
    subgroupAB = pd.merge(subgroupA,subgroupB)
    lengthDataset = len(dataset)
    logging.debug('Examples of the dataset {}'.format(lengthDataset))  
    logging.debug('Examples of subgroup A: {} ({:.2f}%)'.format(len(subgroupA), len(subgroupA)/lengthDataset))
    logging.debug('Examples of subgroup B: {} ({:.2f}%)'.format(len(subgroupB), len(subgroupB)/lengthDataset))
    logging.debug('Examples of subgroup AB: {} ({:.2f}%)'.format(len(subgroupAB), len(subgroupAB)/lengthDataset))
    logging.debug('Examples of subgroup C: {} ({:.2f}%)'.format(len(subgroupC), len(subgroupC)/lengthDataset))

    #Get confidence for A,B -> C
    confAB_C = confidence(subgroupAB, subgroupC)
    logging.debug('Conf(A,B -> C): {:.2f}'.format(confAB_C))

    #Get confidence for B -> C
    confB_C = confidence(subgroupB, subgroupC)
    logging.debug('Conf(B -> C): {:.2f}'.format(confB_C))
    elift = confAB_C / confB_C
    logging.info('Elift: {:.2f}'.format(elift))
    return elift

def confidence(subgroupX,subgroupY):
    """
    Returns the confidence between two subgroups (X -> Y) 
    """
    subgroupXY = pd.merge(subgroupX,subgroupY)
    return len(subgroupXY) / len (subgroupX)