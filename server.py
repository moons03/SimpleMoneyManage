from flask import Flask, request, render_template, redirect, url_for, send_file
import matplotlib.pyplot as plt
import datetime
from calendar import monthcalendar
from random import randint
import json
        
class Expense:
    def __init__(self, amount, data, category):
        self.amount = amount
        self.date = datetime.datetime.strptime(data, "%Y-%m-%d")
        self.category = category
        
class Month:
    def __init__(self, month):
        self.month = month
        days = [day for week in monthcalendar(datetime.datetime.now().year, month) for day in week]
        days = days[days[:7].count(0):]
        self.days = [[] for _ in days]
        self.totalIncome = 0
        self.totalExpense = 0
        self.goals = []
        self.totalCategoryExp = [
            {
                "name": "생활비",
                "categories": ["식비", "쇼핑"],
                "amount": 0
            },
            {
                "name": "고정지출",
                "categories": ["월세", "정기구독", "정기구독 서비스"],
                "amount": 0
            },
            {
                "name": "특별지출",
                "categories": ["생일선물", "선물", "기념일"],
                "amount": 0
            } 
        ]
        
    def dayExpenses(self, day, s=False):
        inc = 0
        exp = 0
        
        for expense in self.days[day - 1]:
            if expense.amount > 0:
                inc += expense.amount
            else:
                for CategoryExp in self.totalCategoryExp:
                    if expense.category in CategoryExp["categories"]:
                        CategoryExp["amount"] += expense.amount * -1
                        break
                
                exp -= expense.amount 
        if s == True:
            inc = f'{inc:,}'
            exp = f'{exp:,}'
        return (inc, exp)
        
    def setGoal(self, category, amount):
        for i in range(len(self.goals)):
            if self.goals[i]["category"] == category:
                self.goals.remove(self.goals[i])
                break
        
        goal = {
            "category": category,
            "goal_amount": amount,
            "amount": 0,
            "done": "X"
        }
        for day in self.days:
            for expense in day:
                if expense.category == category:
                    goal["amount"] += expense.amount
                    
        self.goals.append(goal)
    
def addExpense(year, exp : Expense):
    day = exp.date.day
    month = exp.date.month
    year[month - 1].days[day - 1].append(exp)
    totalIncome = 0
    totalExpense = 0
    for CategoryExp in year[month - 1].totalCategoryExp:
        CategoryExp["amount"] = 0
    
    for day in range(1, len(year[month - 1].days) + 1):
        (income, expense) = year[month - 1].dayExpenses(day)
        totalIncome += income
        totalExpense += expense
    
    for goal in year[month - 1].goals:
        if goal["category"] == exp.category:
            goal["amount"] += exp.amount
            if goal["amount"] >= goal["goal_amount"]:
                goal["done"] = "O"
            break
    
    year[month - 1].totalIncome = totalIncome
    year[month - 1].totalExpense = totalExpense

def MakeGraph(x, y):
    # x = [i for i in range(5, 11)]
    # y = [58400, 68700, 60200, 80000, 90750, 100980]

    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['font.size'] = 20

    plt.figure(figsize=(9, 4))

    plt.plot(x, y, marker='o', markersize=12, linestyle='-', color=(139/255, 69/255, 19/255))

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    plt.xticks(x)
    plt.gca().set_xticklabels([f'{month}월' for month in x], fontweight='bold')
    plt.yticks([])

    plt.tick_params(axis="x", length=0)

    for i, (xi, yi) in enumerate(zip(x, y)):
        plt.plot([xi, xi], [0, yi], linestyle='--', color=(139/255, 69/255, 19/255), linewidth=1.5)
        plt.text(xi, yi + (max(y) // 30), f'{yi:,}', ha='center', va='bottom', fontsize=15, fontweight='600')

    plt.ylim(bottom=min(y) // 2)
    plt.tight_layout()

    plt.savefig('graph.png')
    
year = [None for i in range(13)]
for i in range(1, 13):
    year[i - 1] = Month(i)

def setDefault():
    months = [i for i in range(1, 13)]
    expenses = [58400, 68700, 60200, 80000, 58400, 68700, 60200, 80000, 90750, 68700, 100980, 90750]
    incomes = [i + randint(10000, 50000) for i in expenses]
    for month, income, expense in zip(months, incomes, expenses):
        for i in range(20):
            year[month - 1].setGoal(f"{i}", i)
        if month == 11:
            exp = Expense(1700000, "2023-11-18", "생활비")
            addExpense(year, exp)
            exp = Expense(-80000, "2023-11-18", "식비")
            addExpense(year, exp)
            exp = Expense(-20980, "2023-11-18", "월세")
            addExpense(year, exp)
        year[month - 1].totalIncome = income
        year[month - 1].totalExpense = expense

def read_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for goal in data["Goals"]:
        year[goal["month"] - 1].setGoal(goal["category"], goal["amount"])
        
    for expense in data["Expenses"]:
        exp = Expense(expense["amount"], expense["date"], expense["category"])
        addExpense(year, exp)

# year[8] = Month(8)
# exp = Expense(10000, "2023-8-1", "먀!")
# year[8].addExpense(exp)
# print(year[8].days)

# year[8].setGoal("먀!", 10000)
# year[8].setGoal("먀!", 20000)
# print(year[8].goals)

# amounts = [year[month - 1].totalExpense for month in months]

# MakeGraph(months, amounts)

app = Flask(__name__)

@app.route('/index.html')
def index():
    try:
        month = int(request.args.get("month", datetime.datetime.now().month))
    except Exception:
        redirect("/index.html")
    
    goalExpense = 0
    for goal in year[month - 1].goals:
        goalExpense += goal["goal_amount"]
        
    totalExpense = year[month - 1].totalIncome - year[month - 1].totalExpense
    
    calendar = [0] + [day for week in monthcalendar(datetime.datetime.now().year, month) for day in week]
    if calendar[:7].count(0) == 7:
        calendar = calendar[7:]
    if calendar[:-7].count(0) == 0:
        calendar = calendar + [0] * 6
    else:
        calendar.pop()
    
    calendar = [calendar[i:i+7] for i in range(0, len(calendar), 7)]
    expenses = [year[month - 1].dayExpenses(day, s=True) for day in range(1, len(year[month - 1].days) + 1)]
    
    return render_template('index.html', 
                           month=month, 
                           goalExpense=f'{goalExpense:,}',
                           totalExpense=f'{totalExpense:,}',
                           calendar=calendar,
                           expenses=expenses)

@app.route('/exp_input.html', methods=['GET', 'POST'])
def exp_input():
    try:
        amount = int(request.form.get('amount'))
        transaction_type = request.form.get('transaction-type')
        date = request.form.get('date')
        category = request.form.get('category')
        
        if transaction_type == 'expense':
            amount *= -1
        
        exp = Expense(amount, date, category)
        addExpense(year, exp)
    except Exception:
        render_template('exp_input.html')

    return render_template('exp_input.html')

@app.route('/analysis.html')
def analysis():
    month = datetime.datetime.now().month
    expenses = (f'{year[month - 1].totalIncome:,}', f'{year[month - 1].totalExpense:,}')
    transaction_type = request.args.get('transaction_type', "expense")
    transaction_select = (" selected", "") if transaction_type == 'income' else ("", " selected")
    totalCategoryExp = []
    totalExpense = year[month - 1].totalIncome - year[month - 1].totalExpense
    
    months = list(range(1, 13))
    months = (months[month:] + months[:month])[6:]
    if transaction_type == 'income':
        amounts = [year[m - 1].totalIncome for m in months]
    else:
        amounts = [year[m - 1].totalExpense for m in months]

    MakeGraph(months, amounts)
    
    for categoryExp in year[month - 1].totalCategoryExp:
        totalCategoryExp.append(f'{categoryExp["amount"]:,}')
    return render_template('analysis.html', 
                           expenses=expenses,
                           transaction_select=transaction_select,
                           totalCategoryExp=totalCategoryExp,
                           totalExpense=f'{totalExpense:,}')

@app.route('/graph.png')
def send_graph():
    return send_file('graph.png', mimetype='image/png')

@app.route('/exp_goal_set.html')
def exp_goal_set():
    try:
        month = int(request.args.get('month', ""))
        category = request.args.get('category', "")
        if category == "":
            raise Exception()
        amount = int(request.args.get('amount', ""))
    except Exception:
        return render_template('exp_goal_set.html')
    
    year[month - 1].setGoal(category, amount)
    
    return render_template('exp_goal_set.html')

@app.route('/exp_goal_list.html')
def exp_goal_list():
    month = datetime.datetime.now().month
    return render_template('exp_goal_list.html', month=month, goals=year[month - 1].goals)

# setDefault()
read_json_file("data.json")
app.run('0.0.0.0', port=8000, debug=True)
