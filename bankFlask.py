import json
from datetime import datetime
from random import randint
from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/renderCreateAccForm")
def renderCreateAccFrom():
    return render_template("create.html")

@app.route("/renderDeposit")
def renderDeposit():
    return render_template("deposit.html")

@app.route("/renderWithdraw")
def renderWithdraw():
    return render_template("withdraw.html")

@app.route("/renderInterest")
def renderInterest():
    return render_template("interest.html")

@app.route("/renderTransactions")
def renderTransactions():
    return render_template("transactions.html")

@app.route("/create", methods=["POST"])
def create_account():
    name = request.form['name']
    acc_type = request.form['acctype']
    balance = request.form['balance']
    try:
        acc_num = randint(0, 10000)
        # this is only if the account being created isn't the first
        with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info','r+') as fh:
            all_user_info = json.load(fh)
        person_acc_info = {}
        person_acc_info["Name"] = name
        person_acc_info["Date"] = datetime.today().strftime('%m/%d/%Y')
        person_acc_info["Account Type"] = acc_type
        person_acc_info["Balance"] = int(balance)
        person_acc_info["Starting Balance"] = int(balance)
        all_user_info[acc_num] = person_acc_info

    except:
        acc_num = randint(0, 10000)
        # this is only for the first account being created, because the bank acc info file is empty and doesn't exist
        all_user_info = {}
        person_acc_info = {}
        person_acc_info["Name"] = name
        person_acc_info["Date"] = datetime.today().strftime('%m/%d/%Y')
        person_acc_info["Account Type"] = acc_type
        person_acc_info["Balance"] = int(balance)
        person_acc_info["Starting Balance"] = int(balance)
        all_user_info[acc_num] = person_acc_info
    #with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
        #fh.truncate()
    # truncate empties the file
    with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
        json.dump(all_user_info, fh)
        # dump allows python information to be stored in a json file
    return render_template("acc_created.html")


#'''
#################################################################################################################
@app.route("/deposit", methods=["POST"])
def deposit():
    acc_num = request.form['accnum']
    value = request.form["amt"]
    # this function will also log the transaction
    with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'r') as fh:
        all_user_info = json.load(fh)
    # this is a dictionary of the user's information  ---> ex: {Balance:30, Acc type: checkings}
    user_info = all_user_info[acc_num]
    user_info["Balance"] = int(value) + user_info["Balance"]
    #with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
        #fh.truncate()
    try:
        # this part will have the transaction record if the account user has already made a transaction before.
        # this will add on to the user's transaction record
        with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'r+') as fh:
            transactions_record = json.load(fh)
            # {123:[{},{},{}]  }
        transaction_list = transactions_record[acc_num]
        transaction_info_dict = {}
        transaction_info_dict["Date"] = datetime.today().strftime('%m/%d/%Y')
        transaction_info_dict["Type"] = "Deposit"
        transaction_info_dict["Amount"] = value
        transaction_info_dict["New Balance"] = user_info["Balance"]
        transaction_list.append(transaction_info_dict)
        transactions_record[acc_num] = transaction_list

    except:
        # this part is for when the user is making a transaction for the first time. this will create the user's
        # transaction record
        transactions_record = {}
        transaction_list = []
        transaction_info_dict = {}
        transaction_info_dict["Date"] = datetime.today().strftime('%m/%d/%Y')
        transaction_info_dict["Type"] = "Deposit"
        transaction_info_dict["Amount"] = value
        transaction_info_dict["New Balance"] = user_info["Balance"]
        transaction_list.append(transaction_info_dict)
        transactions_record[acc_num] = transaction_list

    with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
        json.dump(all_user_info, fh)
    with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'w+') as fh:
        json.dump(transactions_record, fh)
    return render_template("depositCompleted.html")


#################################################################################################################

@app.route("/withdraw", methods=["POST"])
def withdraw():
    acc_num = request.form['accnum']
    value = request.form['amt']
    with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'r') as fh:
        all_user_info = json.load(fh)
    user_info = all_user_info[acc_num]
    user_info["Balance"] = user_info["Balance"] - int(value)
    #with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
        #fh.truncate()

    try:
        # this part will have the transaction record if the account user has already made a transaction before. this will add
        # on to the user's transaction record
        with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'r') as fh:
            transactions_record = json.load(fh)
            # {123:[{},{},{}]  }
        transaction_list = transactions_record[acc_num]
        transaction_info_dict = {}
        transaction_info_dict["Date"] = datetime.today().strftime('%m/%d/%Y')
        transaction_info_dict["Type"] = "Withdrawal"
        transaction_info_dict["Amount"] = int(value)
        transaction_info_dict["New Balance"] = user_info["Balance"]
        transaction_list.append(transaction_info_dict)
        transactions_record[acc_num] = transaction_list

    except:
        # this part is for when the user is making a transaction for the first time. this will create the user's transaction record
        transactions_record = {}
        transaction_list = []
        transaction_info_dict = {}
        transaction_info_dict["Date"] = datetime.today().strftime('%m/%d/%Y')
        transaction_info_dict["Type"] = "Withdrawal"
        transaction_info_dict["Amount"] = value
        transaction_info_dict["New Balance"] = user_info["Balance"]
        transaction_list.append(transaction_info_dict)
        transactions_record[acc_num] = transaction_list

    #with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'w+') as fh:
        #fh.truncate()
    with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
        json.dump(all_user_info, fh)

    with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'w+') as fh:
        json.dump(transactions_record, fh)

    return render_template("withdrawCompleted.html")


#################################################################################################################
@app.route("/interest", methods=["POST"])
def interest():
    acc_num = request.form["accnum"]
    later_date = request.form['date']
    today_str_obj = datetime.today().strftime('%m/%d/%Y')
    today_date_obj = datetime.strptime(today_str_obj,'%m/%d/%Y')
    later_date_obj = datetime.strptime(later_date,'%m/%d/%Y')
    delta = later_date_obj-today_date_obj
    try:
        with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'r+') as fh:
            all_user_info = json.load(fh)
        principle = all_user_info[acc_num]["Starting Balance"]
        interest_amt = round(principle*pow((1.0001),delta.days),2)
        all_user_info[acc_num]["Balance"] = all_user_info[acc_num]["Balance"] + interest_amt
        try:
            # this part will have the transaction record if the account user has already made a transaction before. this will add
            # on to the user's transaction record
            with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'r+') as fh:
                transactions_record = json.load(fh)
                # {123:[{},{},{}]  }
            transaction_list = transactions_record[acc_num]
            transaction_info_dict = {}
            transaction_info_dict["Date"] = datetime.today().strftime('%m/%d/%Y')
            transaction_info_dict["Type"] = "Interest"
            transaction_info_dict["Interest Amount"] = interest_amt
            transaction_info_dict["New Balance"] = all_user_info[acc_num]["Balance"]
            transaction_list.append(transaction_info_dict)
            transactions_record[acc_num] = transaction_list

        except:
            # this part is for when the user is making a transaction for the first time. this will create the user's transaction record
            transactions_record = {}
            transaction_list = []
            transaction_info_dict = {}
            transaction_info_dict["Date"] = datetime.today().strftime('%m/%d/%Y')
            transaction_info_dict["Type"] = "Interest"
            transaction_info_dict["Interest Amount"] = interest_amt
            transaction_info_dict["New Balance"] = all_user_info[acc_num]["Balance"]
            transaction_list.append(transaction_info_dict)
            transactions_record[acc_num] = transaction_list

        with open('/Users/medhavijam/PyCharmProjects/flasktest/bank_acc_info', 'w+') as fh:
            json.dump(all_user_info, fh)

        with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'w+') as fh:
            json.dump(transactions_record, fh)

    except:
        y = 0
    return render_template("interestCompleted.html")


#################################################################################################################
# this lets you view all the transactions
@app.route("/transactions", methods=["POST"])
def transactions():
    acc_num = request.form["accnum"]
    with open('/Users/medhavijam/PyCharmProjects/flasktest/transaction_info', 'r') as fh:
        transactions_record = json.load(fh)
    transaction_list = transactions_record[acc_num]
    print (transaction_list)
    headings = ["Date", "Type", "Amount", "New Balance"]
    return render_template("displayTransactions.html", headings = headings, transactions = transaction_list)

#################################################################################################################

# MAKE SURE THAT THIS PIECE OF CODE IS AT THE VERY END BC IF IT'S NOT, THEN THE APPLICATION WON'T BE ABLE TO READ
# ANY OF THE CODE THAT COMES AFTER. THIS IS IMPORTANT!!!!!!!!!!!!!!!!!!
if __name__=='__main__':
   app.run()
