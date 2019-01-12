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
from copy import deepcopy

def induction():
    with open(knowledgeBaseLocation, 'r+') as fp:
        rawKnowledge = json.loads(fp.read())
    # sort knowledge. if next is within the error, record and goes to the next one
    # else go on.
    knowledge = deepcopy(rawKnowledge)
    for k in knowledge:
        k['time'] = datetime.strptime(k['time'], datetimeFormat)
    combine = zip(knowledge, rawKnowledge)
    combine = sorted(combine, key=lambda x: x[0]['time'])
    knowledge, rawKnowledge = zip(*combine)
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

def recordInductiveRulesOne(rawk1, rawk2):
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
                    history = list(set(history))
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
    logging.debug("recordind statement: %s" % rawk)
    k = deepcopy(rawk)
    kID = k['id']
    del k['id']
    del k['time']
    with open(logicIndBaseLocation, 'r+') as fp:
        allLogic = json.loads(fp.read())
    for l in allLogic:
        if l['statement'] == k:
            l['history'].append(kID)
            l['history'] = list(set(l['history']))
            with open(logicIndBaseLocation, 'w+') as fp:
                fp.write(json.dumps(allLogic))
            return
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

if __name__=="__main__":
    logging.basicConfig(filename='interface.log', level=logging.DEBUG, format='%(asctime)-15s %(levelname)s: %(message)s')
    induction()