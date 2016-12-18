"""
Module that includes all the functions for Exceptional Model Mining(EMM)
"""
import logging
import math
from enum import Enum
from sklearn.metrics import matthews_corrcoef

#Define quality measures
QualityMeasure = Enum('Quality Measure', 'SCD')

#Define model class
ModelClass = Enum('Model Class', 'PhiCoefficient')

def emm(dataset):
    """
    Main function for Exceptional Model Mining. Configure the targets to evaluate it
    """

    ####################### CONFIGURE THIS ##############################

    #Define subgroup
    subgroup = dataset[(dataset['browser_colordepth'] < 24.0)]

    #Define target 1
    target1 = 'revenue'

    #Define target 2
    target2 = 'new_buttons'

    #####################################################################

    logging.info("Exceptional Model Mining. (Two targets)")

    lengthDataset = len(dataset)
    logging.debug('Examples of the dataset {}'.format(lengthDataset))  
    logging.debug('Examples of subgroup: {} ({:.2f}%)'.format(len(subgroup), len(subgroup)/lengthDataset))
    correlationTargets = phi_coefficient (dataset,target1,target2)
    logging.debug('Correlation of the two targets: {:.2f}'.format(correlationTargets))
   
    evaluate(QualityMeasure.SCD,ModelClass.PhiCoefficient,dataset,subgroup,target1,target2)

    

def evaluate(QualityMeasure,ModelClass,dataset,subgroup,target1,target2):
    """Execute an evaluation function for a certain quality measure.""" 
    evaluator = {
        QualityMeasure.SCD: evaluate_scd,
    }
    return evaluator.get(QualityMeasure)(ModelClass,dataset,subgroup,target1,target2)


def evaluate_scd (ModelClass,dataset,subgroup,target1,target2):
    """Returns the Significance of Correlation Difference between two targets."""

    #Calculate the complement of the subgroup
    complement = dataset[~dataset.index.isin(subgroup.index)]
     
    if (ModelClass == ModelClass.PhiCoefficient):
        rSubgroup = phi_coefficient (subgroup,target1,target2) 
        rComp = phi_coefficient (complement,target1,target2)
    else:
        rSubgroup = 0
        rComp = 0

    #Apply Fisher transformation to both correlations
    z = fisher_trans (rSubgroup)
    zComp = fisher_trans (rComp)

    n = len(subgroup)
    nComp = len(complement)


    

    if (n < 4 or nComp < 4):
        SCD = 0
    else:
        pValue = ((z - zComp)) / (math.sqrt(    (1/(n-3))  +   (1/(nComp-3))   ))
        SCD = 1 - pValue
    
    logging.info('Correlation subgroup: {:.6f}'.format(rSubgroup))
    logging.info('Correlation complement: {:.6f}'.format(rComp))
    logging.info('SCD: {:.6f}'.format(SCD))

    return SCD

def phi_coefficient (subgroup,target1,target2):
    """Returns the phi coefficient of two targets given a dataset and a subgroup ."""
    return matthews_corrcoef(subgroup[target1], subgroup[target2]) 

def fisher_trans (r):
     """Returns Fisher z transformation."""
     return (1/2) * math.log((1 + r) / (1 - r))

#TODO: Adapt the beam search to EMM
def emm_beamSearch(dataset):
    target1 = 'revenue'
    target2 = 'new_buttons'
    width = 10
    depth = 2 #3
    bins = 4
    categorical_bins = 10
    excluded_columns = [target1,target2]


    subgroups = [(set(), dataset, 0, set())]
    descriptors = []
    columns = set(dataset.columns) - set(excluded_columns)

    for column in columns:
        if (dataset[column].dtype == "float64" or dataset[column].dtype == "int64"):
            descriptors.append((column, getDescriptorsEW(dataset, column, bins)))
        else:
            catbins = []
            dataset[column] = dataset[column].astype('category')
            categories = dataset[column].value_counts().head(categorical_bins)
            for (cat, occurence) in categories.iteritems():
                bin = (dataset[column] == cat)
                binname = column + " = \"" + cat + "\""
                catbins.append((bin, binname))
            descriptors.append((column, catbins))
    #logging.debug(descriptors)
    for level in range(depth):
        logging.debug("level " + str(level))
        newsubgroups = []
        for subgroup in subgroups:
            print(subgroup[0])
            for descriptor in descriptors:
                if not (descriptor[0] in subgroup[0]):
                    columns = subgroup[0] | set([descriptor[0]])
                    for subbin in descriptor[1]:
                        bin = subgroup[1][subbin[0]]
                        val = evaluate_scd(ModelClass.PhiCoefficient,dataset, bin, target1,target2)
                        binname = subgroup[3] | set([subbin[1]])
                        newsubgroup = (columns, bin, val, binname)
                        newsubgroups.append(newsubgroup)
        subgroups = []
        newsubgroups.sort(reverse=True,key=lambda x: x[2])
        seen = set()
        for sg in newsubgroups:
            if (str(sorted(sg[3])) not in seen):
                subgroups.append(sg)
                seen.add(str(sorted(sg[3])))
        subgroups = subgroups[:width]
        for sg in subgroups:
            print(sg[3], sg[2])




def getDescriptorsEW (dataset, column, bins):
    width = (max(dataset[column]) - min(dataset[column]))/bins
    logging.debug("column=" + str(column) + ", width=" + str(width))
    descriptors = []
    start = min(dataset[column]) - 1
    for x in range(bins):
        end = min(dataset[column]) + ((x+1) * width)
        bin = (dataset[column] > start) & (dataset[column] <= end)
        if x == 0:
            binname = column + " < " + str(end)
        elif x == bins - 1:
            binname = column + " >= " + str(start)
        else:
            binname = str(start) + " < " + column + " <= " + str(end)
        #print(start, end)
        #print(bin.value_counts())
        descriptors.append((bin, binname))
        start = end
    return descriptors
