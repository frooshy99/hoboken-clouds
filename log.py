#! python3
# a spending log program.

from time import sleep
import sys
from datetime import date
from datetime import datetime
import openpyxl


def p(text, delay=0.005, end=''):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(delay)


def pi(text):
    print(text, end='')
    sleep(0.05)


def exi(inp):
    if str(inp).casefold() == 'exit' or str(inp).casefold() == 'e':
        p('Goodbye.\n')

        sys.exit()


shortcuts = {'b': 'breakfast',
             'l': 'lunch',
             'd': 'dinner',
             'g': 'groceries',
             'a': 'alcohol'}


monthDic = {1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'}


def month_match(mon):
    monthmonth = monthDic[int(mon)]

    return monthmonth


def space(string):
    length = len(str(string))

    for foo in range(length):
        p(' ')


def space2(datedate):
    length = len(str(datedate)) + 2

    for foo in range(length):
        p(' ')


def stars(num):
    for foo in range(int(num)):
        p('*')

    print()


# this updates time of last entry to the nearest second.
def update():
    f = open(r'C:\Users\theok\AppData\Local\Programs\Python\Python39\pie\logtime.txt', 'w')
    dong = str(datetime.now())[:19]

    f.write(dong)
    f.close()


wbDir = r'C:\Users\theok\AppData\Local\Programs\Python\Python39\pie\logbook.xlsx'
wb = openpyxl.load_workbook(wbDir)
ws = wb.active

# just to get rid of undefined var warnings. ticks me off.
dateVal = ''
year = 0
month = 0
day = 0
name = ''
cost = 0
catCat = 0


def get_row(index):
    global dateVal, year, month, day, name, cost, catCat
    dateVal = str(ws[f'A{int(index)}'].value)

    year = dateVal[:4]

    month = dateVal[5:]
    month = month[:2]
    month = month_match(month)

    day = dateVal[8:]
    day = int(day[:2])

    name = ws[f'B{index}'].value
    cost = ws[f'C{index}'].value
    catCat = ws[f'D{index}'].value


ff = open(r'C:\Users\theok\AppData\Local\Programs\Python\Python39\pie\logtime.txt')
p('Last entry: ')
p(ff.read())

catDic = {1: 'Scotiabank debit',
          2: 'HSBC credit'}

p('\nEnter \'exit\' at any prompt to stop program.\n\n')

p('1 - Add to log\n'
  '2 - View log\n')

while True:
    p('What would you like to do? ')
    choice = input()

    exi(choice)

    # this will be for adding to log
    if int(choice) == 1:
        p('\nHow much did you spend? ')
        val = input()
        exi(val)

        p('What did you spend it on? ')
        name = input()
        exi(name)

        # a shortcut to input breakfast/lunch/dinner,
        if str(name) in shortcuts:
            name = shortcuts[name]

        p('1 - Scotiabank debit\n'
          '2 - HSBC credit\n'
          'Which category would you like to add this to? ')
        cat = input()
        exi(cat)

        d = date.today()

        # should i change this to a while loop? increment x inside.
        for x in range(1, 10000):
            if ws.cell(row=x, column=1).value is None:
                ws[f'A{x}'] = d
                ws[f'B{x}'] = name
                ws[f'C{x}'] = val
                ws[f'D{x}'] = cat

                break
            else:
                continue

        wb.save(wbDir)
        p('\nData added to log.\n')
        update()

        sleep(3)
        p('\n')

        continue

        # so that's one done.

    elif int(choice) == 2:

        # only to initialize numFilled.
        numFilled = 0

        # checks number of filled rows.
        for x in range(1, 10000):
            if ws.cell(row=x, column=1).value is None:
                numFilled = int(x)

                break
            else:
                continue

        yearsList = []

        # for first row.
        get_row(1)

        pi(f'\n{year}:\n'
           f'{month}'
           f' - {day}: ')

        prevYear = year
        prevMonth = month
        prevDay = day

        yearsList.append(int(year))

        pi(f'{name} | ${cost} | ')
        stars(catCat)

        # now to print out the rest of the log
        # sorted by year then month.

        for i in range(2, numFilled):
            get_row(i)

            if int(year) != int(prevYear):
                pi(f'\n{year}:\n')

                prevYear = year
                yearsList.append(int(year))

            if str(month) != str(prevMonth):
                pi(f'{month}')

                prevMonth = month
            else:
                space(month)

            if day != prevDay:
                pi(f' - {day}: ')

                prevDay = day
            else:
                if day < 10:
                    pi('      ')
                else:
                    pi('       ')

            pi(f'{name} | ${cost} | ')
            stars(catCat)

        # now to introduce a filter/sort system
        # let's list down what can be filtered/sorted, then.
        # filter: month, category, cost range
        # sort: cost, category
        # also implement ascending/descending option for sorting,
        # use +/- respectively for input.

        # input()
        # sys.exit()

        # on 2nd thought idk if i even need this
        p('\nFilter/Sort: ')
        fors = input()
        exi(fors)

        if fors.casefold() == 'filter':
            p('1 - Month\n'
              '2 - Payment method\n'
              '3 - Cost range\n'
              'Choose. ')
            filterChoice = input()
            exi(filterChoice)

            # FILTER BY YEAR
            if int(filterChoice) == 1:
                # p(yearsList)

                while True:
                    p('Year: ')
                    yearF = input()
                    exi(yearF)

                    if int(yearF) in yearsList:
                        while True:
                            p('Month (number): ')
                            monIndex = input()
                            exi(monIndex)

                            # remember to do else: error message + continue
                            if 1 <= int(monIndex) <= 12:
                                monName = month_match(monIndex)

                                p(f'Spending for {monName} {yearF}:\n')

                                # adds 0 to a single digit month, for date search on spreadsheet
                                if len(str(monIndex)) == 1:
                                    monIndex = f'0{monIndex}'

                                prevDay = 0

                                for i in range(1, numFilled):
                                    dateVal = str(ws[f'A{i}'].value)

                                    if f'{yearF}-{monIndex}' in dateVal:
                                        day = dateVal[8:]
                                        day = int(day[:2])

                                        name = ws[f'B{i}'].value
                                        cost = ws[f'C{i}'].value
                                        catCat = ws[f'D{i}'].value

                                        if day != prevDay:
                                            pi(f'{day}: {name} | {cost} | {catCat}\n')

                                            prevDay = day
                                        else:
                                            space2(day)
                                            pi(f'{name} | {cost} | {catCat}\n')

                                break
                            else:
                                p('Invalid input. Please try again.\n')

                                continue
                    else:
                        p('Year not found in log. Please try again.\n')

                        continue

            # FILTER BY PAYMENT METHOD
            elif int(filterChoice) == 2:
                while True:
                    p('1 - Scotiabank debit\n'
                      '2 - HSBC credit\n'
                      'Payment method: ')
                    cat = input()
                    exi(cat)

                    if 1 <= int(cat) <= 2:
                        pi(f'{catDic[int(cat)]}:\n')

                        numPrinted = 0

                        for i in range(1, numFilled):
                            get_row(i)

                            if int(catCat) == int(cat):
                                numPrinted += 1

                                if numPrinted < 2:
                                    pi(f'{year}\n'
                                       f'{month} - {day}: '
                                       f'{name} | ${cost} | ')

                                    prevYear = year
                                    prevMonth = month
                                    prevDay = day
                                else:
                                    if int(year) != int(prevYear):
                                        pi(f'\n{year}:\n')

                                        prevYear = year

                                    if str(month) != str(prevMonth):
                                        pi(f'{month}')

                                        prevMonth = month
                                    else:
                                        space(month)

                                    if day != prevDay:
                                        pi(f' - {day}: ')

                                        prevDay = day
                                    else:
                                        pi('      ')

                                    pi(f'{name} | ${cost}\n')
                    else:
                        p('Invalid input. Dumbass.\n'
                          'Please try again.\n')

                        continue

                    break
            # FILTER BY COST RANGE
            elif int(filterChoice) == 3:
                p('Upper limit: ')
                upLim = input()
                exi(upLim)

                p('Lower limit: ')
                lowLim = input()
                exi(lowLim)

                if int(upLim) < int(lowLim):
                    p('Why is the lower limit higher than the upper limit???\n'
                      'You dummy.\n')

                    tempLim = upLim
                    upLim = lowLim
                    lowLim = tempLim

                numPrinted = 0

                for i in range(1, numFilled):
                    get_row(i)

                    if lowLim <= int(cost) <= upLim:
                        p(f'{year}:\n'
                          f'{month} - {day}: ')

                        numPrinted += 1

                        if numPrinted < 2:
                            pi(f'{year}\n'
                               f'{month} - {day}: '
                               f'{name} | ${cost} | ')

                            prevYear = year
                            prevMonth = month
                            prevDay = day
                        else:
                            if int(year) != int(prevYear):
                                pi(f'\n{year}:\n')

                                prevYear = year

                            if str(month) != str(prevMonth):
                                pi(f'{month}')

                                prevMonth = month
                            else:
                                space(month)

                            if day != prevDay:
                                pi(f' - {day}: ')

                                prevDay = day
                            else:
                                pi('      ')

                            pi(f'{name} | ${cost}\n')
        elif fors.casefold() == 'sort':
            p('1+ - Costs, ascending\n'
              '1- - Costs, descending\n'
              '2+ - Categories, ascending\n'
              '2- - Categories, descending\n'
              'Choose. ')
            sortChoice = input()
            exi(sortChoice)

            sortChoice0 = int(str(sortChoice)[0])
            sortChoice1 = str(sortChoice)[1]

            # SORT BY COSTS
            if sortChoice0 == 1:
                costList = []

                # to populate costList, which will then be sorted.
                for i in range(1, numFilled):
                    cost = int(ws[f'C{i}'].value)
                    costList.append(cost)

                # ASCENDING
                if sortChoice1 == '+':
                    costList.sort()
                elif sortChoice1 == '-':
                    costList.sort(reverse=True)

                print(costList)

                listPrinted = []
                j = 0

                while True:
                    # use costList[i] to print row matching w cost
                    # printed row's num added to listPrinted
                    # so row doesn't get printed twice.

                    for i in range(1, numFilled):
                        # found an issue here
                        # j still increments even after break statement on line 464
                        # i have no idea.
                        costMatch = int(costList[j])
                        get_row(i)

                        dateVal = dateVal[:10]

                        if int(cost) == costMatch and i not in listPrinted:
                            p(f'{dateVal} | {name} | {cost} | ')
                            stars(catCat)

                            listPrinted.append(i)
                            j += 1

                            break

                        else:
                            continue

                    if len(listPrinted) == numFilled:
                        break
                    else:
                        continue

            elif sortChoice0 == 2:
                catList = []

                for i in range(1, numFilled):
                    catCat = int(ws[f'D{i}'].value)
                    catList.append(catCat)

                if sortChoice1 == '+':
                    catList.sort()
                elif sortChoice0 == '-':
                    catList.sort(reverse=True)

                listPrinted = []

                while True:
                    for i in range(1, numFilled):
                        catMatch = int(catList[i - 1])
                        get_row(i)

                        if int(catCat) == catMatch and i not in listPrinted:
                            p(f'{dateVal} | {name} | {cost} | ')
                            stars(catCat)

                            listPrinted.append(i)

                    if len(listPrinted) == numFilled:
                        break
                    else:
                        continue
