############################################################
# CIS 521: Homework 7 unit test
############################################################

from sessionization import *
import pytest

############################################################
# Main
############################################################


def main():
    getHeader()
    expiredSessions()
    parseDate()
    print("passed all tests")


############################################################
# test data
############################################################


def getHeader():
    assert getFields(['ip','date','time','zone','cik','accession','extention','code']) == [0, 1, 2, 4, 5, 6]
    assert getFields('dqf') == []
    print("passed getFields")



def parseDate():
    assert dateTimeTryParse(None) == None
    assert dateTimeTryParse('fqwfqf') == None
    print("passed dateTimeTryParse")


def expiredSessions():
    assert getExpiredSessions(None) == set()
    assert getExpiredSessions(1) == set()
    print("passed getExpiredSessions")
    

main()