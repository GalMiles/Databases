# global vars
Tables = ["Customers", "Orders"]
Attributes = ["Customers.Name", "Customers.Age", "Orders.Price", "Orders.Product", "Orders.CustomerName"]
OpList = ['=', '<', '>', '>=', '<=', '<>']
notFound = -1

# functions:
# handling SELECT functions:
def isAttribute(attribute):
    for i in range(0, len(Attributes)):
        if attribute ==Attributes[i]:
            return True
    else:
        return False


def isAttributeList(aList):
    if not aList:  # the list is empty
        return True
    if not isAttribute(aList[0]):
        print("Parsing <attribute_list> failed - invalid")
        exit()
        return False
    return isAttributeList(aList[1:])


def SelectSectionManagement(SelectString):

    if SelectString.startswith('*'):  # if its start with * check if its empty after it
        SelectString = SelectString.strip()
        SelectString = SelectString.replace("*", "")
        if SelectString:  #there is some attribute after * - illegal
            print("Parsing <attribute_list> failed - invalid")
            exit()
            return False
        else:             #if its empty
            return True

    elif SelectString.startswith("DISTINCT"):  # if its start with DISTINCT cut it and sent it to isAttribute
        SelectString = SelectString[8:len(SelectString)]

        if not SelectString:  #check if empty after DISTINCT
            print("Parsing <o_d> failed - invalid")
            exit()
            return False

        elif SelectString.startswith('*'):  # if its start with * check if its empty after it
            SelectString = SelectString.replace('*', '')
            if SelectString:  # there is some attribute after * - illegal
                print("Parsing <attribute_list> failed - invalid")
                exit()
                return False
            else:
                return True
        else:
            return isAttributeList(SelectString.split(','))

    else:
        return isAttributeList(SelectString.split(','))

# handling FROM functions:
def isTable(table):
    for x in range(0, len(Tables)):
        if Tables[x] in table:
            return True
    else:
        print("Parsing <table_list> failed - invalid")
        exit()
        return False


def isTableList(tList):
    if not tList:  # the list is empty
        return True
    if not isTable(tList[0]):
        return False
    return isTableList(tList[1:])


def FromSectionManagement(FromSection):
    return isTableList(FromSection.split(','))


# handling WHERE functions:
def isNumber(numString):
    if(numString.isnumeric()):
        return  True

    if(isString(numString)):
        numString = numString.strip("', /, ")
        if(numString.isnumeric()):
            return True
    return False


def isString(string):
    if string.startswith('/"') and string.endswith('/"'):
        return True
    if string.startswith("'") and string.endswith("'"):
        return True
    if string.startswith("’") and string.endswith("’"):
        return True
    return False


def isConstant(constant):
    if isNumber(constant) or isString(constant) or isAttribute(constant):
        return True
    else:
        print("Parsing <condition> failed - invalid")
        exit()


def isRelOp(Op):
    return Op in OpList


def validSimpleConBrackets(string):
    if not string:  # the String is empty
        return True
    if string.startswith('(') and string.endswith(')'):
        return True
    if (not string.startswith('(')) and (not string.endswith(')')):
        return True
    if string.startswith('(') and (not string.endswith(')')):
        return False
    if (not string.startswith('(')) and string.endswith(')'):
        return False


def validBracketsHelper(String):  # check if string is simple condition
    if "AND" in String or "OR" in String or '(' in String or ')' in String:  # not a simple condition
        return False
    return True


def validBrackets(String):
    if not String:  # the String is empty
        return True
    if len(String) == 1:
        if '(' in String or ')' in String:
            return False
    if validBracketsHelper(String):
        return validSimpleConBrackets(String)
    if String == ")OR)" or String == ")AND)" or String == "(OR(" or String == "(AND)":
        return False

    if (String.startswith(')') or String.startswith('(')) and (not String.endswith(')') and not String.endswith('(')):
        return validBrackets(String[:len(String) - 1])  # shrink the string from the right

    if (String.endswith('(') or String.endswith('(')) and (not String.startswith(')') and not String.startswith('(')):
        return validBrackets(String[1:])  # shrink the string from the left

    if (not String.startswith('(')) and (not String.endswith(')')) or (
            String.startswith('(') and String.endswith(')')) or \
            (String.startswith(')') and String.endswith('(') or (String.startswith('(') and String.endswith('(')) or (
                    String.startswith(')') and String.endswith(')'))):
        return validBrackets(String[1:len(String) - 1])  # shrink the string from both sides

    if String.startswith('(') and (not String.endswith(')')):
        return validBrackets(String[:len(String) - 1])  # shrink the string from the right

    if (not String.startswith('(')) and String.endswith(')'):
        return validBrackets(String[1:])  # shrink the string from the left


def isSimpleCondition(simpleCon):
    OpFound = False
    for x in range(0, len(OpList)):
        if simpleCon.find(OpList[x]):
            OpFound = True
        else:
            print("Parsing <condition> failed - invalid")
            exit()

    # find where op is located
    if OpFound:
        index = -1
        for x in range(0, len(simpleCon)):
            if isRelOp(simpleCon[x]):
                index = simpleCon.index(simpleCon[x])
        if index == -1:
            print("Parsing <condition> failed - invalid")
            exit()
            return False
        op = simpleCon[index]
        firstConstant = simpleCon[:index]
        secondConstant = simpleCon[index + 1:]
        if isConstant(firstConstant) and isRelOp(op) and isConstant(secondConstant):
            if isSameType(firstConstant, secondConstant):  #check if the logic is good and the comparetion is good
              return True
        # print("Parsing <condition> failed")

def isSameType(firstConstant, secondConstant):

    #if its an numeric attribute
    if ((isNumberAttribute(firstConstant) and isNumber(secondConstant)) or (isNumberAttribute(secondConstant) and isNumber(firstConstant))):
        return True

    #if its a string attribute
    elif ((firstConstant==Attributes[0]) and (not isNumber(secondConstant)) or ((firstConstant==Attributes[3]) and (not isNumber(secondConstant)))or ((firstConstant==Attributes[4])) and (not isNumber (secondConstant))) or ((secondConstant==Attributes[0]) and (not isNumber(firstConstant)))or ((secondConstant == Attributes[3]) and (not isNumber(firstConstant)))or ((secondConstant ==Attributes[4]) and (not isNumber(firstConstant))):
        return True

    else:
        print("Parsing <condition> failed - invalid")
        exit()
        return False


def isStringAttribute(attribute):
    if ((Attributes[0] == attribute) or (Attributes[4] == attribute) or (Attributes[5] == attribute)):
        return True
    return False

def isNumberAttribute(attribute):
    if ((Attributes[1] == attribute) or (Attributes[2] == attribute)):
        return True
    return False


def isCondition(cList):
    if not cList:  # the list is empty
        return True
    # check every condition for brackets
    if not isSimpleCondition(cList[0]):
        return False
    return isCondition(cList[1:])


def WhereSectionManagement(WhereString):
    # checking if there is an empty condition (like: A>5 AND (nothing))
    if WhereString.startswith("AND") or WhereString.startswith("OR") or WhereString.endswith("AND") \
            or WhereString.startswith("OR"):
        print("Parsing <condition> failed - invalid")
        exit()
    else:
        # splitting the string to a list using "AND", "OR"
        # so that we won't need a multiple parameters split function
        if not validBrackets(WhereString):
            print("Parsing <condition> failed - invalid")
            exit()
            return False
        #at this stage, the brackets are valid. now to remove them
        WhereString = WhereString.replace(")", "").replace("(", "")
        #continue with the condition check
        WhereString = WhereString.replace("AND", "|").replace("OR", "|")
        WhereSectionList = WhereString.split("|")
        if isCondition(WhereSectionList):
            return True
        print("Parsing <condition> failed - invalid")
        exit()
        return False


def inputHandling(query):
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
    if not Where.endswith(';'):
        return None
    return [Select, From, Where]


def inputManagement(myInput):
    myList = inputHandling(myInput)
    if myList is None:
        print("Query need to end with ';' - invalid")
        exit()
        return False

    else:
        #get rid of the ';'
        myList[2] = myList[2][:len(myList[2]) - 1]
        isWhereTrue = isWhereLogicTrue(myList)
        isSelectTrue = isSelectLogicTrue(myList)

        if(isWhereTrue and isSelectTrue):
            SelectSection = SelectSectionManagement(myList[0])
            FromSection = FromSectionManagement(myList[1])
            WhereSection = WhereSectionManagement(myList[2])

            if (FromSection and WhereSection and SelectSection):
                return True
            else:
                 return False

        else:
            if (not isSelectTrue):
                print("Parsing <attribute_list> failed - invalid")
                exit()
            elif(not isWhereTrue):
                print("Parsing <condition> failed - invalid")
                exit()
            return False

def isWhereLogicTrue(myList):
    isOk = False

    if ((myList[1].find("Customers") != notFound) and (myList[1].find("Orders") != notFound)):  # if there are both tables
        if ((myList[2].find("Customers") != notFound) or ((myList[2].find("Orders") != notFound))):  # if Cutomers/Orders in WHERE part
            isOk = True

    elif ((myList[1].find("Customers") != notFound)):  # there is only Customers table
        if ((myList[2].find("Customers") != notFound) and (myList[2].find("Orders") == notFound)):  # check WHERE part
            isOk = True

    elif ((myList[1].find("Orders") != notFound)):  # there is only Orders table
        if ((myList[2].find("Orders") != notFound) and (myList[2].find("Customers") == notFound)):  # check WHERE part
            isOk = True

    return isOk;
def isSelectLogicTrue(myList):
    isSelect = False

    if ((myList[1].find("Customers") != notFound) and (myList[1].find("Orders") != notFound)):  # if there are both tables
        if ((myList[0].find("Customers") != notFound) or ((myList[0].find("Orders") != notFound))):
            isSelect = True

    elif ((myList[1].find("Customers") != notFound)):  # there is only Customers table
        if ((myList[0].find("Customers") != notFound)):
            isSelect = True


    elif ((myList[1].find("Orders") != notFound)):  # there is only Orders table
        if ((myList[0].find("Orders") != notFound)):
            isSelect = True

    if(not isSelect):
        if (myList[0].find("*") != notFound):
            isSelect = True
        elif(myList[0].find("DISTINCT") != notFound): #if we are here in the select we dont have attribute or * only DISTINCT
            print("Parsing <o_d> failed - invalid")
            exit()
    return isSelect

def main():
    query = input("Please enter a Query:")
    queryList = [query]

    if (inputManagement(queryList[0])):
        print("valid")

if __name__ == '__main__':
    main()
