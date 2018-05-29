import csv
import collections
from datetime import datetime
import collections
import heapq
from dateutil.parser import parse
import os.path


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MY STRATEGY:
# i will declare two data structures
# 1st is  dictionary(visitsDict) that stores key value pair of ip address and a list of [session start time,
# session duration till now, number of visits till now ,order], order is the order that request was read
# 2nd shall be a min heap(heapOfLastAccess) of a tuple containing session latest time, ip address
# whenever we see a next line from log file, we compare its time with heap-top if time difference is
# greater than timeout, we keep extrating heap top till time difference from heap top is < timeout
# Now we check via ip address(that is 2nd value in tuple of heap) into our dict and delete all these elements
# from dict too and eventually paste them to sessionization.txt.
# Also if the latest read line's ip was not in dict previously, we just add it to both heap and dict.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# global variables

# timeout refers to session duration
timeout = 0

# heap is min heap that stores latest access time for a particular ip address
heapOfLastAccess = []


# this dictionary contains  key value for ip address and corresponding data for a session
visitsDict = collections.OrderedDict()


def dateTimeTryParse(value):
    try:
        return parse(value)
    except:
        return None


def writeToFile(lst, sessionFile):
    # write to text file
    if sessionFile is not None and lst is not None:
        for e in lst:
            sessionFile.write(e[1])


def getFields(row):
    """ 
    following methods orders timeout fields into a list  
    Arguments:
        row {[list]} -- [description]
    Returns:
        [list] -- [list of indexes]
    """
    lstIndexes = []
    if row is not None:
        for i, itm in enumerate(row):
            if itm == 'ip':
                lstIndexes.append(i)
                break
        for i, itm in enumerate(row):
            if itm == 'date':
                lstIndexes.append(i)
                break
        for i, itm in enumerate(row):
            if itm == 'time':
                lstIndexes.append(i)
                break
        for i, itm in enumerate(row):
            if itm == 'cik':
                lstIndexes.append(i)
                break
        for i, itm in enumerate(row):
            if itm == 'accession':
                lstIndexes.append(i)
                break
        for i, itm in enumerate(row):
            if itm == 'extention':
                lstIndexes.append(i)
                break
    return lstIndexes


def getExpiredSessions(visittime):
    s = set()
    if not isinstance(visittime, datetime):
        return s
    while len(heapOfLastAccess) >= 1:
        top = heapOfLastAccess[0]
        if (visittime - top[0]).total_seconds() > timeout:
            s.add(top)
            heapq.heappop(heapOfLastAccess)
        else:
            break
    return s


with open(os.path.dirname(__file__) + '/../input/inactivity_period.txt', 'r') as inactivityFile:
    timeout = int(inactivityFile.readline())

with open(os.path.dirname(__file__) + '/../output/sessionization.txt', 'w') as sessionFile:
    with open(os.path.dirname(__file__) + '/../input/log.csv', "r") as csvfile:
        datareader = csv.reader(csvfile)
        count = -1
        # visits Dictionary has each key with 4 values, start datetime, recent datetime, session duration till now, visits till now
        fields = []  # fields will store order of all fields
        for row in datareader:
            if count == -1:
                fields = getFields(row)
            else:
                if len(row) >= 6:
                    ip = row[fields[0]]
                    visittime = dateTimeTryParse(
                        row[fields[1]] + ' ' + row[fields[2]])
                    cae = str(row[fields[3]]) + \
                        str(row[fields[4]]) + str(row[fields[5]])
                    if isinstance(visittime, datetime) and visittime is not None and len(cae) > 0 and len(ip) > 0:
                        # get expired sessions from heap
                        allExpired = getExpiredSessions(visittime)
                        if len(allExpired) > 0:
                            # 'delete these from dict, insert into file and look what to do with new element in next if statement'
                            lst = []
                            for elem in allExpired:
                                l = visitsDict[elem[1]][:4]
                                st = ''.join([',' + str(elem)
                                              for elem in l]) + '\n'
                                lst.append(
                                    (visitsDict[elem[1]][4], elem[1] + st))
                                del visitsDict[elem[1]]
                            lst = sorted(lst)
                            writeToFile(lst, sessionFile)
                        if ip in visitsDict:
                            # means session of this ip is still maintained
                            # update the heap
                            # put into heap with new values of recent time 
                            # heapify now
                            if (visitsDict[ip][1], ip) in heapOfLastAccess:
                                index = heapOfLastAccess.index((visitsDict[ip][1], ip))
                                heapOfLastAccess[index] = (visittime, ip)
                                heapq.heapify(heapOfLastAccess)
                            # updating dictionary item
                            visitsDict[ip][1] = visittime
                            visitsDict[ip][2] = int(
                                (visittime - visitsDict[ip][0]).total_seconds() + 1)
                            visitsDict[ip][3] += 1
                        else:
                            # put into heap with new values of recent time
                            heapq.heappush(heapOfLastAccess, (visittime, ip))
                            visitsDict[ip] = [
                                visittime, visittime, 1, 1, count]
            count += 1
        if len(visitsDict) > 0:
            # these are left over items in dictionary when file end is reached
            lst = []
            for k, v in visitsDict.items():
                l = v[:4]
                st = ''.join([',' + str(elem) for elem in l]) + '\n'
                lst.append((v[4], k+st))
            lst = sorted(lst)
            writeToFile(lst, sessionFile)

	