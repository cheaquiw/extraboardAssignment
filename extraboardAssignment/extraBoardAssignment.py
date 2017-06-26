
# Get the Date from the User
year = 2017
while True:
    try:
        month = int(input('Please enter the month as a number'))
        break
    except ValueError:
        print('Please try again')
while True:
    try:
        day = int(input('Please enter the day'))
        break
    except ValueError:
        print('Please try again')


#Open Runs (made up, will import from actual database automatically)
openRun = [('115/161', 'dtc/dtc', '05:05 - 13:30'),('160', 'dtc/dtc', '05:10 - 17:00'), ('161', 'delWebb/dtc', '05:10 - 13:40'), ('183', 'delWebb/delWebb', '05:15 - 14:00'), ('134', 'dtc/dtc', '06:00 - 15:00')]

#List of All Drivers (made up, will import from actual database automatically)
operator = [(153, 'plumb', 'sick'), (163, 'burke', 'extraboard'), (179, 'stefanovich', 'extraboard'),
             (192, 'edward', 'extraboard'), (201, 'henderson', 'extraboard'),
             (202, 'sergy', 'extraboard'), (211, 'burgett', 'extraboard'), (221, 'wiedemeier', 'sick'),
             (225, 'sherrod', 'extraboard'), (226, 'fuchs', 'extraboard'), (229, 'cheaqui', 'extraboard'), (233, 'parker', 'extraboard'),
             (234, 'martinez', 'extraboard'), (232, 'Schaffer', '186'), (230, 'Smith', 117),
             (228, 'Foyle', '173')]
operator = sorted(operator)

#Number of Days Monday Through Friday Excluding Holidays, to be Used in Calculating the Redline Order
def numberDaysMF(year, month, day):
    import datetime
    startDate = datetime.date(2017, 5, 14)
    date_configuring = datetime.date(year, month, day)
    daydiff = date_configuring.weekday() - startDate.weekday()
    if datetime.date(2017, 7, 4) <= date_configuring:
        daydiff = daydiff - 2
    elif datetime.date(2017, 5, 29) <= date_configuring:
        daydiff = daydiff - 1
    days = int(((date_configuring - startDate).days - daydiff) / 7 * 5 + min(daydiff, 5) - (max(date_configuring.weekday() - 4, 0) % 5))
    return days

numDays = numberDaysMF(year, month, day)

# Add Number of Drivers on Redline
def addBoard(operator):
    board = 0
    for driver in operator:
        board = sum(1 for x in operator if 'extraboard' in x) + sum(1 for x in operator if 'Vacation Relief' in x)
        vacation = sum(1 for x in operator if 'vacation' in x or 'sick' in x)
        board = board - vacation
    return board
boardNumber = addBoard(operator)

# Calculates Which Operators are a Part of the Redline
def redlineOp(operator):
    x = []
    for driver in operator:
        if 'sick' and 'vacation' not in driver and 'extraboard'in driver or 'Vacation Relief' in driver:
            x.append(driver[:2])
    return x

redOp = redlineOp(operator)

#Assign Open Work to Available ExtraBoard in Redline Order
def assignOpenWork(openRun, redLineOrder):
    assignment = []
    assignment = [redLineOrder[ix] + openRun[ix] for ix in range(len(openRun))]
    return assignment

# Assign Report Time to Remaining ExtraBoard Operators in Redline Order
def assignRepTimes(repOps, repTimes):
    assignment = [repOps[ix] + repTimes[ix] for ix in range(len(repTimes))]
    return assignment

# Number of ExtraBoard Operators on Report
def reportOperators():
    numReportOperators = len(redlineOp(operator))-len(openRun)
    return numReportOperators

reportOps = reportOperators()

# Calculate Report Times Based on Number of Report Operators
def reportTimes(reportOperators):
    if reportOperators == 0:
        list = 0
    elif reportOperators == 1:
        list = [('05:05', 'DelWebb')]
    elif reportOperators == 2:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb')]
    elif reportOperators == 3:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb')]
    elif reportOperators == 4:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:45', 'DelWebb')]
    elif reportOperators == 5:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:45', 'DelWebb'), ('10:35', 'DelWebb')]
    elif reportOperators == 6:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:45', 'DelWebb'), ('10:35', 'DelWebb'), ('12:30', 'DelWebb')]
    elif reportOperators == 7:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:45', 'DelWebb'), ('10:35', 'DelWebb'), ('11:30', 'DelWebb'), ('12:30', 'DelWebb')]
    elif reportOperators == 8:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:45', 'DelWebb'), ('10:35', 'DelWebb'), ('11:30', 'DelWebb'), ('12:30', 'DelWebb'), ('13:30', 'DelWebb')]
    return list

repTimes = reportTimes(reportOperators())

# assign order of operators by redline and date (e.g. (Current_date-beginning_date-weekends-holidays)%number_of_operators...
redLineOrder = (redlineOp(operator)[+numberDaysMF(year, month, day)%boardNumber:] + redlineOp(operator)[:+numberDaysMF(year, month, day)%boardNumber])

assignedRuns = assignOpenWork(openRun, redLineOrder)

'''
# Runs Sorted by First Time Off, Pay, and Spread in that Order for the First 32 Runs
run112 = 0
run113 = 1
run116 = 2
run115 = 3
run111 = 4
run108 = 5
run114 = 6
run168 = 7
run169 = 8
run106 = 9
run103 = 10
run104 = 11
run153 = 12
'''
# 102'107', '101', '105', '109', '170', '110', '151', '159', '157', '160', '152', '158', '155', '163', '145', '164', '161', '162']

# Group Variables to Make it Easier to Work With and Follow
assignedWork = assignOpenWork(openRun, redLineOrder)
repOps = redLineOrder[-reportOperators():]

assignedReport = assignRepTimes(repOps, repTimes)

assignedTotalWork = assignedWork + assignedReport
print(assignedTotalWork)

#9 hour rule