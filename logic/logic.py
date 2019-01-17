''' 
the idea is that this deduces the relation between a statement and another statement
and puts it in a database. come to think of it, the database cant say the probability
it can only say how many times this happenned and that happenned in the same time.
induction and such get the general rules, and thhere will be another function that 
generates real knowledge
'''
from settings import *
import json
import logging
from datetime import datetime, timedelta
sameTimeError = timedelta(milliseconds=1000) # milisec
datetimeFormat = "%Y-%m-%d %H:%M:%S.%f"
highProbability = 0.8
from copy import deepcopy

def induction():
    with open(knowledgeBaseLocation, 'r+') as fp:
        rawKnowledge = json.loads(fp.read())
    # sort knowledge. if next is within the error, record and goes to the next one
    # else go on.

    # knowledge = deepcopy(rawKnowledge)
    # for k in knowledge:
    #     k['time'] = datetime.strptime(k['time'], datetimeFormat)
    # combine = zip(knowledge, rawKnowledge)
    # combine = sorted(combine, key=lambda x: x[0]['time'])
    # knowledge, rawKnowledge = zip(*combine)
    knowledge, rawKnowledge = knowledgeSort(rawKnowledge)
    # logging.debug("sorted knowledge %s" % knowledge)
    logging.debug("sorted raw knowledge %s" % str(rawKnowledge))
    for i in range(len(knowledge)):
        try:
            n=0
            while 1:
                n+=1
                currentDT = knowledge[i]['time']
                comparingDT = knowledge[i+n]['time']
                if comparingDT - currentDT <= sameTimeError:
                    # record as same time
                    k2 = rawKnowledge[i+n]
                    k1 = rawKnowledge[i]
                    recordStatement(k1)
                    recordStatement(k2)
                    logging.debug("same time: %s and %s" % (str(k1), str(k2)))
                    recordInductiveRules(k1, k2)
                else:
                    break
        except IndexError:
            logging.debug("Index Error i+n=%d, len=%s" % (i+n, len(knowledge)))

def recordInductiveRulesOne(rawk1, rawk2,):
    k1 = deepcopy(rawk1)
    k2 = deepcopy(rawk2)
    logging.debug("recording inductive rule one %s and %s" % (str(k1), str(k2)))
    with open(logicIndBaseLocation, 'r+') as fp:
        allLogic = json.loads(fp.read())
    k1ID = k1['id']
    k2ID = k2['id']
    del k1['id']
    del k2['id']
    del k1['time']
    del k2['time']
    # see if k1 already exists
    for l in allLogic:
        # if it does, see if k2 already exists
        if l["statement"] == k1:
            logging.debug("statement does exist: %s" % (k1))
            for r in l['relation list']:
                if r["statement"] == k2:
                    history = [tuple(h) for h in r['history']]
                    history.append((k1ID, k2ID))
                    logging.debug("history: %s" % history)
                    try:
                        history = list(set(history))
                    except TypeError:
                        # logging.debug("complex history!")
                        # historyJson = [json.dumps(h) for h in history]
                        # historyJson = list(set(historyJson))
                        # history = [json.loads(h) for h in historyJson]
                        # logging.debug("setted history: %s" % history)
                        history = complexHistorySet(history)
                    r['history'] = history
                    with open(logicIndBaseLocation, 'w+') as fp:
                        fp.write(json.dumps(allLogic))
                    return
            l['relation list'].append({"statement": k2, 'history': [(k1ID, k2ID)]})
            with open(logicIndBaseLocation, 'w+') as fp:
                fp.write(json.dumps(allLogic))
                return
    logging.debug("statement doesnt exist: %s" % (k1))
    logging.debug("all logic: %s" % (allLogic))

def recordInductiveRules(k1, k2):
    logging.debug("recording inductive rule %s and %s" % (str(k1), str(k2)))
    recordInductiveRulesOne(k1, k2)
    recordInductiveRulesOne(k2, k1)

def recordStatement(rawk):
    logging.debug("recording statement: %s" % rawk)
    k = deepcopy(rawk)
    kID = k['id']
    del k['id']
    del k['time']
    with open(logicIndBaseLocation, 'r+') as fp:
        allLogic = json.loads(fp.read())
    for l in allLogic:
        if l['statement'] == k:
            logging.debug("already exist, adding %s" % str(kID))
            l['history'].append(kID)
            try:
                l['history'] = list(set(l['history']))
            except TypeError:
                l['history'] = complexHistorySet(l['history'])
            logging.debug("history now: %s" % l['history'])
            with open(logicIndBaseLocation, 'w+') as fp:
                fp.write(json.dumps(allLogic))
            return
    logging.debug("doesnt exist: %s" % str(kID))
    newRule = {
        "statement": k,
        "history": [kID],
        "relation list": []
    }
    allLogic.append(newRule)
    with open(logicIndBaseLocation, 'w+') as fp:
        fp.write(json.dumps(allLogic))

def concludeInd(statement):
    try:
        del statement['id']
        del statement['time']
    except KeyError:
        pass
    with open(logicIndBaseLocation, "r+") as fp:
        allLogic = json.loads(fp.read())
    for l in allLogic:
        if l['statement'] == statement:
            matchLogic = deepcopy(l)
            break
    conclusionList = []
    for r in matchLogic['relation list']:
        r['statement']['source'] = "induction"
        r['statement']['probability'] = len(r['history'])/len(matchLogic['history'])
        r['statement']['number of data'] = len(matchLogic['history'])
        conclusionList.append(r['statement'])
    return conclusionList

def findCombineFactors(statementDict):
    logging.debug("trying to find combined factors for %s" % statementDict)
    rl = statementDict["relation list"]
    history = statementDict['history']
    factorHistoryList = []
    factorList = []
    for r in rl: # get all the factors
        if len(r['history'])/len(history) >= highProbability:
            factorList.append(r)
            logging.debug("high probability factor: %s" % r)
            for theID in list(set([h[1] for h in r['history']])):
                factorHistoryList.append(findByID(theID))
    factorHistoryList, _ = knowledgeSort(factorHistoryList)
    for h in history: # see if the new concept is true in history
        k1 = findByID(h)
        logging.debug("history knowledge: %s" % str(k1))
        occurTime = datetime.strptime(k1['time'], datetimeFormat)
        statementsNow = []
        statementsNowFull = []
        logging.debug("factor history list: %s" % str(factorHistoryList))
        for f in factorHistoryList:
            factorHistoryTime = f['time']
            if factorHistoryTime - occurTime <= sameTimeError:
                if factorHistoryTime - occurTime >= timedelta(milliseconds=0):
                    logging.debug("factor history time: %s" % str(factorHistoryTime))
                    fCopy = deepcopy(f)
                    del fCopy['time']
                    # fCopy2 = deepcopy(fCopy)
                    del fCopy['id']
                    statementsNow.append(fCopy)
                    statementsNowFull.append(deepcopy(f))
                # next step, make duplicates in the same time go away
            else:
                break
        logging.debug("same time as %s: %s" % (k1, statementsNow))
        logging.debug(str(factorList))
        if dictListCompare(statementsNow, [f['statement'] for f in factorList]):
            logging.debug("combined factors true, recording")
            combinedFactors = {
                "mode": "combined factors",
                "id": [s.pop('id') for s in statementsNowFull],
                "children statements": statementsNow,
                "time": datetime.strftime(statementsNowFull[-1]['time'], datetimeFormat)
            }
            recordStatement(combinedFactors)
            recordInductiveRules(k1, combinedFactors)
        else:
            logging.debug("combined factors doesn't exist")

def knowledgeSort(rawKnowledge):
    logging.debug("sorting knowledge: %s" % rawKnowledge)
    knowledge = deepcopy(rawKnowledge)
    for k in knowledge:
        k['time'] = datetime.strptime(k['time'], datetimeFormat)
    combine = zip(knowledge, rawKnowledge)
    combine = sorted(combine, key=lambda x: x[0]['time'])
    knowledge, rawKnowledge = zip(*combine)
    logging.debug("knowledge: %s\nraw knowledge: %s" % (knowledge, rawKnowledge))
    return knowledge, rawKnowledge

def findBy(what, matchesWhat): # for knowledge base
    with open(knowledgeBaseLocation, "r+") as fp:
        knowledgebase = json.loads(fp.read())
    matchItems = []
    for k in knowledgebase:
        if k[what] == matchesWhat:
            matchItems.append(k)
    return matchItems

def findByID(theID):
    logging.debug("finding ID: %d" % theID)
    matchItems = findBy("id", theID)
    if matchItems == []:
        logging.debug("found nothing")
        return None
    logging.debug("found %s" % matchItems[0])
    return matchItems[0]

def dictListCompare(list1Raw, list2Raw):
    list1 = deepcopy(list1Raw)
    list2 = deepcopy(list2Raw)
    if len(list1) != len(list2):
        return False
    
    i1 = list1[0]
    if len(list1) > 1:
        for i2 in list2:
            if i1 == i2:
                list1.remove(i1)
                list2.remove(i2)
                return dictListCompare(list1, list2)
    else:
        return i1 == list2[0]
    return False
    
def complexHistorySet(history):
    logging.debug("complex history!")
    historyJson = [json.dumps(h) for h in history]
    historyJson = list(set(historyJson))
    history = [json.loads(h) for h in historyJson]
    logging.debug("setted history: %s" % history)
    return history

if __name__=="__main__":
    logging.basicConfig(filename='interface.log', level=logging.DEBUG, format='%(asctime)-15s %(levelname)s: %(message)s')
    induction()
