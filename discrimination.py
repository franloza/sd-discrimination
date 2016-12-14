"""
Module that includes all the commong functions for discrimination detection
"""
import logging
import pandas as pd

def discrimination(dataset,indirect_discrimination=False):

    ####################### CONFIGURE THIS ##############################

    #Create subgroup A (Containing sensitive information)
    subgroupA = dataset[(dataset['attractive_o'] <=6)]
    #subgroupA = dataset[(dataset['age'] >= 31)]
    #subgroupA = dataset[(dataset['attractive_o'] <= 4)] 

    #Create subgroup B (Containing predictive information)
    subgroupB = dataset[(dataset['like'] >= 8)]
    #subgroupB = dataset[(dataset['interests_correlate'] > 0.4)]
   
    #Create subgroup D (Containing information correlated to A) [Only indirect discrimination]
    subgroupD = dataset[(dataset['attractive_important'] <=10)] 

    #####################################################################

    #Create subgroup C (Label)
    subgroupC = dataset[dataset['match'] == 1]

    lengthDataset = len(dataset)
    logging.info("Discrimination detection")
    logging.debug('Examples of the dataset {}'.format(lengthDataset))  
    
    if not (indirect_discrimination):
        logging.info("Direct discrimination")
        logging.debug('Examples of subgroup A: {} ({:.2f}%)'.format(len(subgroupA), len(subgroupA)/lengthDataset))
        logging.debug('Examples of subgroup B: {} ({:.2f}%)'.format(len(subgroupB), len(subgroupB)/lengthDataset))
        logging.debug('Examples of subgroup C: {} ({:.2f}%)'.format(len(subgroupC), len(subgroupC)/lengthDataset))
        elift(dataset,subgroupA,subgroupB,subgroupC)
    else:
        logging.info("Indirect discrimination")
        subgroupA = pd.merge(subgroupA,subgroupD)
        subgroupDB = pd.merge(subgroupD,subgroupB)
        logging.debug('Examples of subgroup A: {} ({:.2f}%)'.format(len(subgroupA), len(subgroupA)/lengthDataset))
        logging.debug('Examples of subgroup B: {} ({:.2f}%)'.format(len(subgroupB), len(subgroupB)/lengthDataset))
        logging.debug('Examples of subgroup C: {} ({:.2f}%)'.format(len(subgroupC), len(subgroupC)/lengthDataset))
        logging.debug('Examples of subgroup D: {} ({:.2f}%)'.format(len(subgroupD), len(subgroupD)/lengthDataset))
        confDB_A = confidence(subgroupDB, subgroupA)
        logging.debug('Conf(D,B -> A): {:.2f}'.format(confDB_A))
        elift(dataset,subgroupA,subgroupB,subgroupC)

def elift (dataset, subgroupA, subgroupB, subgroupC):
    """
    Returns the elift measure of the subgroup AB with respect to a label (C)
    """

    #Get subgroup A,B
    subgroupAB = pd.merge(subgroupA,subgroupB)
    lengthDataset = len(dataset)
    logging.debug('Examples of subgroup AB: {} ({:.2f}%)'.format(len(subgroupAB), len(subgroupAB)/lengthDataset))

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