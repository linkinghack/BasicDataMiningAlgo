from ConfigReader import Configure
from tqdm import tqdm
import logging
import logging.handlers


# setup logging
handler = logging.handlers.RotatingFileHandler('kNN.log',maxBytes=2*1024*1024,backupCount=5) 
fmt = '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)s -  %(message)s' 
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# model
class Record(object):
    def __init__(self,features,lable):
        self.features = features
        self.lable = lable
        self.dist = 0

    def __str__(self):
        return "features: " + str(self.features) + " lable: " + str(self.lable)
    def toDistString(self):
        return self.__str__() + " dist: " + self.dist

# read config
OPTION = Configure.readConfig('config.json')

# utils
def readData(file):
    records = list()
    for line in file:
        templine = [float(i) for i in line.split(OPTION['seprator'])]
        features = list()
        for feature in templine[OPTION['col_of_features'][0]:OPTION['col_of_features'][1]]:
            features.append(feature)
        record = Record(features,templine[OPTION['col_of_class_lable']]) #construct a record
        records.append(record)
    return records

def HammingDist(a,b):
    if len(a) != len(b):
        return None
    else:
        dist = 0
        for i in range(0,len(a),1):
            if(a[i] == b[i]):
                dist += 1
        return dist

def EuclidDist(a,b):
    if len(a) != len(b):
        return None
    else:
        dist = 0
        for i in range(0,len(a),1):
            dist += (a[i] - b[i]) ** 2
        #dist = math.sqrt(dist)
        return dist

def main():
    # construct training dataset
    TrainingDataFile = open(OPTION['trainingDataSource'])
    TrainingData = readData(TrainingDataFile)
    TrainingDataFile.close()

    # read target data and apply kNN algorithm
    TargetDataFile = open(OPTION['targetDataSource'])
    TargetData = readData(TargetDataFile)
    TargetDataFile.close()

    correctCount = 0

    # classify
    K = OPTION['k']
    hamming = OPTION['hamming_dist']
    if hamming:
        logger.info('using hamming distance.')
    for record in tqdm(TargetData,desc='Progress',leave=False,mininterval=2,maxinterval=4,miniters=0):
        logger.info('--------------')
        logger.info(record)
        logger.info('Classify result: ')
        neighours = dict()
        for base in TrainingData:
            if hamming:
                base.dist = HammingDist(base.features,record.features)
            else:
                base.dist = EuclidDist(base.features,record.features)
        # sort and find kNN
        TrainingData.sort(key = lambda item: item.dist)
        for i in range(0,K,1):
            lable = TrainingData[i].lable
            if lable in neighours.keys():
                neighours[lable] += 1
            else:
                neighours[lable] = 1
        logger.info('KNN: {lable: count}')
        logger.info(str(neighours))
        # detect the nearest
        neighbourlist = list(neighours.items())
        neighbourlist.sort(key=lambda item: item[1],reverse=True)
        logger.info('judgement: This record belongs to class : ' + str(neighbourlist[0][0]) + " correct? : " + str(neighbourlist[0][0]==record.lable) )
        if neighbourlist[0][0] ==  record.lable:
            correctCount +=1
        logger.info('-------------')
    print('Correct Rate: ',correctCount/len(TargetData))
    logger.info('Correct Rate: '+str(correctCount/len(TargetData)))

main()