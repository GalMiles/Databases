import random
import re


Tables = ["R", "S"]
Attributes = ["R.A", "R.B", "R.C", "R.D", "R.E",
              "S.D", "S.E", "S.F", "S.H", "S.I"]
RAttributes = ["R.A", "R.B", "R.C", "R.D", "R.E"]
SAttributes = ["S.D", "S.E", "S.F", "S.H", "S.I"]
delimiter = " ,"
# logical operators display
AND = " AND "
OR = " OR "
# comperason operators display
EQUALS = " = "

rule11bConditions = ["R.D = S.D AND R.E = S.E", "R.D = S.D AND S.E = R.E", "S.D = R.D AND R.E = S.E",
                     "S.D = R.D AND S.E = R.E", "R.E = S.E AND R.D = S.D", "R.E = S.E AND S.D = R.D",
                     "S.E = R.E AND S.D = R.D", "S.E = R.E AND R.D = S.D"]
agreedAtrributesE = ["S.E = R.E", "R.E = S.E"]
agreedAtrributesD = ["S.D = R.D", "R.D = S.D"]

FILE_NAME = "statistics.txt"
IntBytes = 4

n_VAL = 0
R_VAL = 1
V_FileFirstIndex = 2  # index that starts the V list of scheme


class PI:
    OpName = "PI"
    attributes = []
    activated = False

    def __init__(self, attributeList):
        self.activated = True
        self.attributes = attributeList

    def printOp(self):
        OpString = self.OpName + "["
        for i in range(0, len(self.attributes)):
            OpString = OpString + self.attributes[i]
            if i != len(self.attributes) - 1:
                OpString = OpString + delimiter
        OpString = OpString + "]"
        print(OpString, end="")


class SIGMA:
    OpName = "SIGMA"
    argsList = []
    activated = False
    isSIGMAR = False
    isSIGMAS = False

    def __init__(self, conditionString):
        self.activated = True
        self.argsList.clear()
        self.argsList.append(conditionString)

    def setArgsList(self, argsList):
        self.argsList = argsList

    def getArgsList(self):
        return self.argsList

    # for adding the closing brackets in the algebraic expression print
    def getArgsListLen(self):
        return len(self.argsList)

    # here we need to print the argList instead of the conditions
    def printOp(self):
        OpString = ""
        if self.isSIGMAR:
            return 0
        elif self.isSIGMAS:
            return 0
        else:
            for condition in self.argsList:
                OpString = OpString + self.OpName + "[" + condition + "]"
                print(OpString, end="")


class CARTESIAN:
    OpName = "CARTESIAN"
    schemes = Tables
    tables = []
    activated = False
    isSIGMAR = False
    isSIGMAS = False

    def __init__(self, tableString):
        self.activated = True
        self.tables = tableString

    def printOp(self):
        OpString = self.OpName
        if (self.isSIGMAR == True) and (self.isSIGMAS == False):  # SIGMA inside CARTESIAN
            print("CARTESIAN(", end="")
            print("SIGMA[" + self.tables[0] + "](R)", end="")  # print SIGMA
            print("," + self.tables[1] + ")", end="")
        elif (self.isSIGMAS == True) and (self.isSIGMAR == False):
            print("CARTESIAN(" + self.tables[0] + ",SIGMA[", end="")
            print(self.tables[1] + "](S))", end="")
        elif (self.isSIGMAS == True) and (self.isSIGMAR == True):
            print("CARTESIAN(SIGMA[" + self.tables[0] + "](R),SIGMA[" + self.tables[1] + "](S))", end="")
        else:
            print("CARTESIAN(", end="")
            print(self.tables[0] + "," + self.tables[1] + ")", end="")


class NJOIN:
    OpName = "NJOIN"
    schemes = Tables
    tables = []
    activated = False
    isSIGMAR = False
    isSIGMAS = False

    def __init__(self, tableList):
        self.activated = True
        self.tables = tableList

    def printOp(self):
        OpString = self.OpName
        if (self.isSIGMAR == True) and (self.isSIGMAS == False):  # SIGMA inside CARTESIAN
            print("NJOIN(", end="")
            print("SIGMA[" + self.tables[0] + "](R)", end="")  # print SIGMA
            print("," + self.tables[1] + ")", end="")
        elif (self.isSIGMAS == True) and (self.isSIGMAR == False):
            print("NJOIN(" + self.tables[0] + ",SIGMA[", end="")
            print(self.tables[1] + "](S))", end="")
        elif (self.isSIGMAS == True) and (self.isSIGMAR == True):
            print("NJOIN(SIGMA[" + self.tables[0] + "](R),SIGMA[" + self.tables[1] + "](S))", end="")
        else:
            print("NJOIN(", end="")
            print(self.tables[0] + "," + self.tables[1] + ")", end="")


# each of these 3 functions splits the string to a list
def FromSectionManagement(FromString):
    return FromString.split(',')


def SelectSectionManagement(SelectString):
    return SelectString.split(',')


def WhereSectionManagement(WhereString):
    WhereString = WhereString.replace("AND", AND).replace("OR", OR).replace("=", EQUALS)
    return WhereString


def queryHandling(query):
    # remove ; if necessary
    if query.endswith(";"):
        query = query[:len(query) - 1]
    # separate the 3 lines (sections)
    query = query.replace(" ", "")  # removing spaces
    endOfSelect = query.index('FROM')
    endOfFrom = query.index('WHERE')
    Select = query[:endOfSelect]
    From = query[endOfSelect:endOfFrom]
    Where = query[endOfFrom:]
    # removing the query words and spaces
    Select = Select.replace("SELECT", "", 1)
    From = From.replace("FROM", "", 1)
    Where = Where.replace("WHERE", "", 1)
    return [Select, From, Where]


def printExpressionList(expressionList):
    bracesCount = 0
    for i in range(0, len(expressionList)):
        if expressionList[i].OpName in ["PI", "SIGMA"]:
            res = expressionList[i].printOp()
            if res != 0:
                print("(", end="")
                bracesCount = bracesCount + 1

        elif expressionList[i].OpName in ["CARTESIAN", "NJOIN"]:
            expressionList[i].printOp()
    for i in range(0, bracesCount):
        print(")", end="")
    print("\n")

def printExpList(expressionList):
    for expression in expressionList:
        print(expression.OpName)
        if type(expression) is SIGMA:
            print(expression.argsList)
        elif type(expression) is CARTESIAN:
            print(expression.schemes)
        elif type(expression) is PI:
            print(expression.attributes)
        elif type(expression) is NJOIN:
            print(expression.schemes)


# PART 1 FUNCTIONS

def rule6(algExpressionList):
    CARTESIANIndex = findCARTESIANIndex(algExpressionList)
    NJOINIndex = findNJOINIndex(algExpressionList)

    if (CARTESIANIndex > NJOINIndex):  # we have CARTESIAN
        optionalSIGMAIndex = CARTESIANIndex - 1
        optionalSIGMA = algExpressionList[optionalSIGMAIndex]
        if (optionalSIGMA.OpName == "SIGMA"):
            # SIGMA before CARTESIAN
            if (isRPredicat(optionalSIGMA.argsList)):  # check if its R's predicat
                algExpressionList[CARTESIANIndex].tables[0] = algExpressionList[optionalSIGMAIndex].argsList[0]
                algExpressionList[CARTESIANIndex].isSIGMAR = True
                algExpressionList[optionalSIGMAIndex].isSIGMAR = True
                swapItems(algExpressionList, optionalSIGMAIndex, CARTESIANIndex)


    else:  # we have NJOIN
        optionalSIGMAIndex = NJOINIndex - 1
        optionalSIGMA = algExpressionList[optionalSIGMAIndex]
        if (optionalSIGMA.OpName == "SIGMA"):  # SIGMA before NJOIN
            if (isRPredicat(optionalSIGMA.argsList)):  # check if its R's predicat
                algExpressionList[NJOINIndex].tables[0] = algExpressionList[optionalSIGMAIndex].argsList
                algExpressionList[NJOINIndex].isSIGMAR = True
                algExpressionList[optionalSIGMAIndex].isSIGMAR = True
                swapItems(algExpressionList, optionalSIGMAIndex, NJOINIndex)


def rule6a(algExpressionList):
    CARTESIANIndex = findCARTESIANIndex(algExpressionList)
    NJOINIndex = findNJOINIndex(algExpressionList)

    if (CARTESIANIndex > NJOINIndex):  # we have CARTESIAN
        optionalSIGMAIndex = CARTESIANIndex - 1
        optionalSIGMA = algExpressionList[optionalSIGMAIndex]
        if (optionalSIGMA.OpName == "SIGMA"):  # SIGMA before CARTESIAN
            if (isSPredicat(optionalSIGMA.argsList)):  # if its S's predicat
                algExpressionList[CARTESIANIndex].tables[1] = algExpressionList[optionalSIGMAIndex].argsList[0]
                algExpressionList[CARTESIANIndex].isSIGMAS = True
                algExpressionList[optionalSIGMAIndex].isSIGMAS = True
                swapItems(algExpressionList, optionalSIGMAIndex, CARTESIANIndex)


    else:  # we have NJOIN
        optionalSIGMAIndex = NJOINIndex - 1
        optionalSIGMA = algExpressionList[optionalSIGMAIndex]
        if (optionalSIGMA.OpName == 'SIGMA'):  # SIGMA before NJOIN
            if (isSPredicat(optionalSIGMA.argsList)):  # check if its S's predicat
                algExpressionList[NJOINIndex].tables[1] = algExpressionList[optionalSIGMAIndex].argsList[0]
                algExpressionList[NJOINIndex].isSIGMAS = True
                algExpressionList[optionalSIGMAIndex].isSIGMAS = True
                swapItems(algExpressionList, optionalSIGMAIndex, NJOINIndex)


def rule5a(algExpressionList):
    PIIndex = findPIIndex(algExpressionList)
    optionalSIGMAIndex = PIIndex + 1
    attributesSIGMAList = []
    isLegal = False
    if (algExpressionList[optionalSIGMAIndex].OpName == 'SIGMA'):  # there is SIGMA after PI
        for i in range(0, len(algExpressionList[optionalSIGMAIndex].argsList)):  # creating attributeSIGMAList
            for j in range(0, len(Attributes)):
                if ((Attributes[j] in algExpressionList[optionalSIGMAIndex].argsList[i]) and (
                        Attributes[j] not in attributesSIGMAList)):
                    attributesSIGMAList.append(Attributes[j])

        for i in range(0, len(attributesSIGMAList)):  # checking if all attributes in SIGMA are in PI
            for j in range(0, len(algExpressionList[PIIndex].attributes)):
                if (attributesSIGMAList[i] in algExpressionList[PIIndex].attributes):
                    isLegal = True
                else:
                    isLegal = False
        if (isLegal == True):
            swapItems(algExpressionList, PIIndex, optionalSIGMAIndex)


def rule11b(algExpressionList):
    CARTESIANIndex = findCARTESIANIndex(algExpressionList)
    optionalSIGMAIndex = CARTESIANIndex - 1

    optionalSIGMA = algExpressionList[optionalSIGMAIndex]
    if (optionalSIGMA.OpName == "SIGMA"):  # if there is SIGMA before CARTESIAN
        if (optionalSIGMA.argsList[0] in rule11bConditions):  # the column are all agreed in S and R
            tableList = algExpressionList[CARTESIANIndex].tables
            nodeNJOIN = NJOIN(tableList)
            nodeNJOIN.isSIGMAR = algExpressionList[CARTESIANIndex].isSIGMAR
            nodeNJOIN.isSIGMAS = algExpressionList[CARTESIANIndex].isSIGMAS
            algExpressionList[optionalSIGMAIndex] = nodeNJOIN
            del algExpressionList[CARTESIANIndex]

        # the condition S.E=R.E AND R.D=S.D is seperate by two SIGMA'S
        elif (algExpressionList[optionalSIGMAIndex - 1].OpName == "SIGMA"):  # check if there are two SIGMAS
            condition1 = algExpressionList[optionalSIGMAIndex - 1].argsList[0]
            condition2 = algExpressionList[optionalSIGMAIndex].argsList[0]
            if (((condition1 in agreedAtrributesE) and (condition2 in agreedAtrributesD)) or (
                    (condition1 in agreedAtrributesD) and (condition2 in agreedAtrributesE))):
                tableList = algExpressionList[CARTESIANIndex].tables
                nodeNJOIN = NJOIN(tableList)
                nodeNJOIN.isSIGMAR = algExpressionList[CARTESIANIndex].isSIGMAR
                nodeNJOIN.isSIGMAS = algExpressionList[CARTESIANIndex].isSIGMAS
                algExpressionList[optionalSIGMAIndex - 1] = nodeNJOIN
                del algExpressionList[CARTESIANIndex]
                del algExpressionList[optionalSIGMAIndex]


def isRPredicat(list):
    if "S" in list[0]:  # not only R's attributes
        return False
    return True


def isSPredicat(list):
    if "R" in list[0]:
        return False
    return True


def findPIIndex(algExpressionList):
    index = -1
    for i in range(0, len(algExpressionList)):
        if algExpressionList[i].OpName == 'PI':
            index = i
            return index
    return index


def findSIGMAIndex(algExpressionList):
    index = -1
    for i in range(0, len(algExpressionList)):
        if algExpressionList[i].OpName == 'SIGMA':
            index = i
            return index
    return index


def findNJOINIndex(algExpressionList):
    index = -1
    for i in range(0, len(algExpressionList)):
        if algExpressionList[i].OpName == 'NJOIN':
            index = i
            return index
        return index


def findCARTESIANIndex(algExpressionList):
    index = -1
    for i in range(0, len(algExpressionList)):
        if algExpressionList[i].OpName == 'CARTESIAN':
            index = i
            return index
    return index


def splitStringByMainANDOperator(conditionString):
    if conditionString.startswith('(') and conditionString.endswith(')'):
        conditionString = conditionString[1:len(conditionString) - 1]
    lenOfAND = len(AND)
    # find the main bracket
    mainBracket = findMainBrackets(conditionString)
    if mainBracket is None:
        print("Rule 4 error.")
        exit()
    # now we need to split the conditions according to the main brackets location
    tempConditionString = conditionString.strip('(').strip(')')
    tempMainBracket = mainBracket.strip('(').strip(')')
    mainBracketsIndex = conditionString.find(mainBracket)

    # main bracket in the beginning of the argsList
    if tempConditionString.startswith(tempMainBracket):
        mainBracket = mainBracket[1:len(mainBracket) - 1]  # remove opening and closing brackets from the condition
        restOfTheConditions = conditionString[len(mainBracket) + 1 + lenOfAND + 1:]
        return [mainBracket, restOfTheConditions]
    # main bracket in the end of the argsList
    elif tempConditionString.endswith(tempMainBracket):
        mainBracket = mainBracket[1:len(mainBracket) - 1]  # remove opening and closing brackets from the condition
        restOfTheConditions = conditionString[:len(conditionString) - (len(mainBracket) + 1) - (lenOfAND + 1)]
        return [restOfTheConditions, mainBracket]
    # main bracket in the middle of the argsList
    else:
        restOfTheConditionsBeg = conditionString[:mainBracketsIndex - lenOfAND]
        restOfTheConditionsEnd = conditionString[mainBracketsIndex + len(mainBracket):]
        return [restOfTheConditionsBeg, mainBracket + restOfTheConditionsEnd]


def splitListByMainANDOperator(argsList):
    if len(argsList) == 1:  # it's just the condition string
        if '(' in argsList[0] and ')' in argsList[0]:
            return splitStringByMainANDOperator(argsList[0])
        else:  # split by the first AND
            firstANDIndex = argsList[0].find(AND)
            return [argsList[0][:firstANDIndex], argsList[0][firstANDIndex + len(AND):]]
    else:  # we are dealing with a list, need to find main brackets in list of strings
        # find the first brackets in list of strings
        for i in range(0, len(argsList)):
            if '(' in argsList[i] and ')' in argsList[i]:
                conditionsToAdd = splitStringByMainANDOperator(argsList[i])
                argsList[i:i + 1] = conditionsToAdd
                return argsList
            else:  # split by the first AND
                if AND in argsList[i]:
                    firstANDIndex = argsList[i].find(AND)
                    conditionsToAdd = [argsList[i][:firstANDIndex], argsList[i][firstANDIndex + len(AND):]]
                    argsList[i:i + 1] = conditionsToAdd
                    return argsList


def findMainBrackets(String):
    if len(String) == 1 or not String:
        return None
    # dealing with: 2 brackets: (condition) AND (condition)
    twoBracketsStringCheck = ')' + AND + '('
    if twoBracketsStringCheck in String:
        if not String.startswith('('):
            String = '(' + String
            return findMainBrackets(String[:len(String) - 1])

    if String.startswith('(') and String.endswith(')'):
        return String

    if not String.startswith('(') and not String.endswith(')'):
        return findMainBrackets(String[:len(String) - 1])
    elif String.startswith('(') and not String.endswith(')'):
        return findMainBrackets(String[:len(String) - 1])
    elif String.endswith(')') and not String.startswith(')'):
        return findMainBrackets(String[1:])
    else:
        return findMainBrackets(String[1:len(String) - 1])


def rule4(algExpression):
    if (not isSIGMAInAlgExp(algExpression)):
        return
    SIGMAIndex = findSIGMAIndex(algExpression)
    newList = algExpression[SIGMAIndex].argsList

    # make the argsList to a string
    conditionString = ""
    for i in range(0, len(newList)):
        conditionString = conditionString + newList[i]

    if AND in conditionString:
        updatedArgsList = splitListByMainANDOperator(newList)
        list1 = [updatedArgsList[0]]
        list2 = [updatedArgsList[1]]
        algExpression[SIGMAIndex].setArgsList(list1)
        newNode = SIGMA(list2)
        newNode.setArgsList(None)
        newNode.setArgsList(list2)
        algExpression.insert(SIGMAIndex + 1, newNode)  # add node to list


def rule4a(algExpression):
    if (not isSIGMAInAlgExp(algExpression)):
        return
    index1 = findSIGMAIndex(algExpression)
    if len(algExpression) == index1 + 1:
        return
    if algExpression[index1 + 1].OpName == "SIGMA":  # we have SIGMA,SIGMA nodes
        swapItems(algExpression, index1, (index1 + 1))


def swapItems(list, indexA, indexB):
    temp = list[indexA]
    list[indexA] = list[indexB]
    list[indexB] = temp


# PART 2 FUNCTIONS

def createAlgExpressionList(queryList):
    return [PI(SelectSectionManagement(queryList[0])), SIGMA(WhereSectionManagement(queryList[2])),
            CARTESIAN(FromSectionManagement(queryList[1]))]


def tenTimesRandomRulesOnAlgExpr(algExpressionList):
    for i in range(0, 10):
        # generate random choice from 'a' to 'e'
        randChoice = chr(random.randrange(97, 97 + 5))

        if randChoice == 'a':
            print("Rule number 4:                ", end="")
            rule4(algExpressionList)
            printExpressionList(algExpressionList)
        elif randChoice == 'b':
            print("Rule number 4a:               ", end="")
            rule4a(algExpressionList)
            printExpressionList(algExpressionList)
        elif randChoice == 'c':
            print("Rule number 6:                ", end="")
            rule6(algExpressionList)
            printExpressionList(algExpressionList)
            print("Rule number 6a:               ", end="")
            rule6a(algExpressionList)
            printExpressionList(algExpressionList)
        elif randChoice == 'd':
            print("Rule number 5a:               ", end="")
            rule5a(algExpressionList)
            printExpressionList(algExpressionList)
        elif randChoice == 'e':
            print("Rule number 11b:              ", end="")
            rule11b(algExpressionList)
            printExpressionList(algExpressionList)
    print("-------------------------------------------------")


# PART 3 FUNCTIONS


def getFileInput(schemeName):
    res = []
    f = open(FILE_NAME, "r")
    for x in f:
        if schemeName in x:
            scheme = f.readline()
            scheme_RValue = scheme.count("INTEGER") * IntBytes
            for i in range(0, scheme.count(':') + 1):
                if i == R_VAL:
                    res.append(scheme_RValue)
                numbersOfLine = re.findall(r"[-+]?\d*\.\d+|\d+", f.readline())
                res.append(int(numbersOfLine[0]))

            return res


def getAttributesFromFile(schemeName):
    res = []
    f = open(FILE_NAME, "r")
    for x in f:
        if schemeName in x:
            scheme = f.readline()
            numOfAttributes = scheme.count("INTEGER")
            SchemeAttribute = scheme[0]
            currentAttributeOfSchemeIndex = 2
            spaceBetweenAttributesOfScheme = len(":INTEGER,") + 1
            # if scheme name is R than put R.
            for i in range(0, numOfAttributes):
                res.append(SchemeAttribute + "." + scheme[currentAttributeOfSchemeIndex])
                currentAttributeOfSchemeIndex = currentAttributeOfSchemeIndex + spaceBetweenAttributesOfScheme
            return res


def getNumOfAttributesFromFile(schemeName):
    res = []
    f = open(FILE_NAME, "r")
    for x in f:
        if schemeName in x:
            scheme = f.readline()
            return scheme.count("INTEGER")


# this method get the sigmaNumber sigma from the list
def getSigmaByNumber(algExpressionList, numberOfWhichSigma):
    sigmaNumber = 0
    index = -1

    for i in range(0, len(algExpressionList)):
        if algExpressionList[i].OpName == 'SIGMA':
            sigmaNumber = sigmaNumber + 1
            if numberOfWhichSigma == sigmaNumber:
                index = i

    return algExpressionList[index]


def countSigmas(algExpressionList):
    count = 0
    for i in range(0, len(algExpressionList)):
        if algExpressionList[i].OpName == 'SIGMA':
            count = count + 1
    return count


def getPi(algExpression):
    for i in range(0, len(algExpression)):
        if "PI" in algExpression[i].OpName:
            return algExpression[i]


def isNJOINInAlgExp(algExpression):
    for i in range(0, len(algExpression)):
        if "NJOIN" in algExpression[i].OpName:
            return True
    return False


def isSIGMAInAlgExp(algExpression):
    for i in range(0, len(algExpression)):
        if "SIGMA" in algExpression[i].OpName:
            return True
    return False


def numberOfPiAttributes(algExpressionList):
    pi = getPi(algExpressionList)
    return len(pi.attributes)


def buildVList(schemeName):
    FileInput = getFileInput(schemeName)
    numOfRAttributes = getNumOfAttributesFromFile(schemeName)

    VList = []
    for i in range(0, numOfRAttributes):
        VList.append(FileInput[(V_FileFirstIndex + i)])
    return VList


def getCalcConditionProbFromNextSigma(algExpressionList, sigmaCounter):
    RAttributesFromFile = getAttributesFromFile("Scheme R")
    SAttributesFromFile = getAttributesFromFile("Scheme S")

    # build matching prob of attributes:

    R_VList = buildVList("Scheme R")
    S_VList = buildVList("Scheme S")

    calcConditionProb = 0

    sigma = getSigmaByNumber(algExpressionList, sigmaCounter + 1)
    argsList = sigma.argsList

    for currentCondition in argsList:
        # check if simple condition
        if AND not in currentCondition and OR not in currentCondition:

            j = 0
            for attribute in SAttributesFromFile:
                if attribute in currentCondition:
                    calcConditionProb = S_VList[j]
                j = j + 1
            j = 0
            for attribute in RAttributesFromFile:
                if attribute in currentCondition:
                    calcConditionProb = R_VList[j]
                j = j + 1

        # not a simple condition
        else:
            # convert AND into *  ,  convert OR into +
            currentCondition = currentCondition.replace(AND, '|*|').replace(OR, '|+|')
            currentConditionList = currentCondition.split('|')  # convert to list

            # convert the every condition to its prob
            for k in range(0, len(currentConditionList)):
                currentVal = currentConditionList[k]
                j = 0
                for attribute in SAttributesFromFile:
                    if str(attribute) in str(currentVal):
                        currentConditionList[k] = S_VList[j]
                    j = j + 1
                j = 0
                for attribute in RAttributesFromFile:
                    if str(attribute) in str(currentVal):
                        currentConditionList[k] = R_VList[j]
                    j = j + 1

            # convert the list of strings to string and evaluate expression
            currentCondition = ""
            for currentVal in currentConditionList:
                currentCondition = currentCondition + str(currentVal)
            calcConditionProb = eval(currentCondition)
    return calcConditionProb


def menu():
    return input("Which rule do you want to activate?\n"
                 " a - rule number 4\n"
                 " b - rule number 4a\n"
                 " c - rule number 6, 6a\n"
                 " d - rule number 5a\n"
                 " e - rule number 11b\n")


def activateRule(menuVal, algExpressionList):
    if menuVal == 'a':
        print("Rule number 4:                ", end="")
        rule4(algExpressionList)
        printExpressionList(algExpressionList)

    elif menuVal == 'b':
        print("Rule number 4a:               ", end="")
        rule4a(algExpressionList)
        printExpressionList(algExpressionList)


    elif menuVal == 'c':
        print("Rule number 6:                ", end="")
        rule6(algExpressionList)
        printExpressionList(algExpressionList)


        print("Rule number 6a:               ", end="")
        rule6a(algExpressionList)
        printExpressionList(algExpressionList)


    elif menuVal == 'd':
        print("Rule number 5a:                 ", end="")
        rule5a(algExpressionList)
        printExpressionList(algExpressionList)


    elif menuVal == 'e':
        print("Rule number 11b:                ", end="")
        rule11b(algExpressionList)
        printExpressionList(algExpressionList)


    else:
        print("Wrong input.")
        exit()



def sizeEstimation(algExpressionList, originalAlgExpressionList):
    printExpressionList(algExpressionList)
    # reverse the lists
    algExpressionList = algExpressionList[::-1]
    originalAlgExpressionList = originalAlgExpressionList[::-1]

    RFileInput = getFileInput("Scheme R")
    SFileInput = getFileInput("Scheme S")
    n_R = RFileInput[n_VAL]
    n_S = SFileInput[n_VAL]
    R_R = RFileInput[R_VAL]
    R_S = SFileInput[R_VAL]

    currInput_n = 0
    currOutput_n = 0
    currInput_R = 0
    currOutput_R = 0

    inputCounter = 0
    outputCounter = 1
    sigmaCounter = 0
    firstOperator = True

    n_SigmaList = []
    for operator in algExpressionList:
        if firstOperator:
            if type(operator) is CARTESIAN:
                currOutput_n = n_R * n_S
                currOutput_R = R_R + R_S
            elif type(operator) is SIGMA:
                calcConditionProb = getCalcConditionProbFromNextSigma(algExpressionList, sigmaCounter)
                currOutput_n = int(max(n_R, n_S) / calcConditionProb)  # worst case
                n_SigmaList.append(currOutput_n)
                currOutput_R = max(R_S, R_R)  # worst case
                sigmaCounter = sigmaCounter + 1
            elif type(operator) is NJOIN:  # NJOIN == cartesian+sigma,  input of cartesian, output of sigma
                calcConditionProb = getCalcConditionProbFromNextSigma(originalAlgExpressionList, sigmaCounter)
                currOutput_n = int(max(n_R, n_S) / calcConditionProb)  # worst case
                # n_SigmaList.append(currOutput_n)
                currOutput_R = max(R_S, R_R)  # worst case
                sigmaCounter = sigmaCounter + 1

            print(operator.OpName)
            print("input:  n_R =", n_R, "| n_S =", n_S, "| R_R =", R_R, "| R_S =", R_S)
            print("output: n_Scheme1 =", currOutput_n, "| R_Scheme1 =", currOutput_R, '\n')
            firstOperator = False
        else:
            currInput_n = currOutput_n
            currInput_R = currOutput_R

            print(operator.OpName)

            if type(operator) is CARTESIAN:
                currOutput_R = R_R + R_S

                if 'R' in operator.tables and 'S' in operator.tables:
                    currOutput_n = n_R * n_S
                if 'R' in operator.tables:  # so the other table is some SIGMA
                    n_S = currInput_n
                    currOutput_n = n_R * n_S
                elif 'S' in operator.tables:  # so the other table is some SIGMA
                    n_R = currInput_n
                    currOutput_n = n_R * n_S
                elif not ('R' in operator.tables and 'S' in operator.tables):  # get number of lines from both sigmas
                    n_R = n_SigmaList[0]
                    n_S = n_SigmaList[1]
                    if n_R or n_S == 0:
                        currOutput_n = max(n_R, n_S)
                    else:
                        currOutput_n = n_R * n_S

                print("input:  n_R", inputCounter, "=", n_R, "| n_S", inputCounter, "=", n_S, "| R_R", inputCounter, "=", R_R, "| R_S", inputCounter, "=", R_S)
            else:
                print("input:  n_Scheme", inputCounter, "=", currInput_n, "| R_Scheme", inputCounter, "=", currInput_R)

            if type(operator) is PI:
                currOutput_n = currInput_n
                currOutput_R = IntBytes * numberOfPiAttributes(algExpressionList)
            elif type(operator) is SIGMA:
                calcConditionProb = getCalcConditionProbFromNextSigma(algExpressionList, sigmaCounter)
                currOutput_n = int(currInput_n / calcConditionProb)
                n_SigmaList.append(currOutput_n)
                currOutput_R = currInput_R
                sigmaCounter = sigmaCounter + 1



            print("output: n_Scheme", outputCounter, "=", currOutput_n, "| R_Scheme", outputCounter, "=", currOutput_R,
                  '\n')

        inputCounter = inputCounter + 1
        outputCounter = outputCounter + 1
    print("-----------------------------------------------------")


def main():
    # PART1
    query = input("Please enter query: ")
    queryList = queryHandling(query)
    print("SQL->algebraic expression:    ", end="")
    algExpressionList = createAlgExpressionList(queryList)
    printExpressionList(algExpressionList)
    menuVal = menu()
    activateRule(menuVal, algExpressionList)

    # PART2
    input("Press Enter to continue to different random logical query plans    >>")
    algExpr1 = createAlgExpressionList(queryList)
    tenTimesRandomRulesOnAlgExpr(algExpr1)
    algExpr2 = createAlgExpressionList(queryList)
    tenTimesRandomRulesOnAlgExpr(algExpr2)
    algExpr3 = createAlgExpressionList(queryList)
    tenTimesRandomRulesOnAlgExpr(algExpr3)
    algExpr4 = createAlgExpressionList(queryList)
    tenTimesRandomRulesOnAlgExpr(algExpr4)

    # printing the 4 different expressions we got:
    print("First expression:          ", end="")
    printExpressionList(algExpr1.copy())
    print("Second expression:         ", end="")
    printExpressionList(algExpr2.copy())
    print("Third expression:          ", end="")
    printExpressionList(algExpr3.copy())
    print("Fourth expression:         ", end="")
    printExpressionList(algExpr4.copy())
    print("-------------------------------------------------")

    # PART3
    input("Press Enter to continue to size estimations    >>")
    newOriginalAlgExpressionList1 = createAlgExpressionList(queryList).copy()
    sizeEstimation(algExpr1, newOriginalAlgExpressionList1)
    newOriginalAlgExpressionList2 = createAlgExpressionList(queryList).copy()
    sizeEstimation(algExpr2, newOriginalAlgExpressionList2)
    newOriginalAlgExpressionList3 = createAlgExpressionList(queryList).copy()
    sizeEstimation(algExpr3, newOriginalAlgExpressionList3)
    newOriginalAlgExpressionList4 = createAlgExpressionList(queryList).copy()
    sizeEstimation(algExpr4, newOriginalAlgExpressionList4)




if __name__ == '__main__':
    main()
