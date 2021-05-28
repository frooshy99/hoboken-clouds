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


# feel free to add any shortcuts
shortcuts = {'b': 'breakfast',
             'l': 'lunch',
             'd': 'dinner'}


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


wbDir = '[XLSX FILE LOCATION]'
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


ff = open('[TXT FILE FOR DATETIME OF LAST ENTRY]')
p('Last entry: ')
p(ff.read())

# feel free to change this to whatever
catDic = {1: 'debit card',
          2: 'credit card'}

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

        # for shortcuts
        if str(name) in shortcuts:
            name = shortcuts[name]

        p('1 - debit card\n'
          '2 - credit card\n'
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

        # filter/sort functionality removed for now.

        
