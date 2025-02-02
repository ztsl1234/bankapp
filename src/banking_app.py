import logging
from datetime import datetime

from utils import utils
from bank_acc import BankAccount

logger = logging.getLogger(__name__)

"""
# Bank Account

You're designing a simple banking system that handles operations on bank accounts. The system should be capable of the following features:
- input banking transactions
- calculate interest
- printing account statement

All the example below assumes console input/output is used. 


When launching the application, it prompts user for actions:
```
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

User should be able to enter `T` or `t` to select input transactions menu. Similarly, initial character is used for other options.

## Input transactions
Upon selecting Input transactions option, application prompts user for transaction details.
```
Please enter transaction details in <Date> <Account> <Type> <Amount> format 
(or enter blank to go back to main menu):
>
```

User is then able to enter something like the following:
```
20230626 AC001 W 100.00
```
The system should automatically create the account when the first transaction for the account is created.

Some constraints to note:
* Date should be in YYYYMMdd format
* Account is a string, free format
* Type is D for deposit, W for withdrawal, case insensitive
* Amount must be greater than zero, decimals are allowed up to 2 decimal places
* An account's balance should not be less than 0. Therefore, the first transaction on an account should not be a withdrawal, and any transactions thereafter should not make balance go below 0
* Each transaction should be given a unique id in YYYMMdd-xx format, where xx is a running number (see example below)

Then system responds by displaying the statement of the account:
(assuming there are already some transactions in the account)
```
Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |
| 20230601 | 20230601-01 | D    | 150.00 |
| 20230626 | 20230626-01 | W    |  20.00 |
| 20230626 | 20230626-02 | W    | 100.00 |

Is there anything else you'd like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

## Define interest rule
Upon selecting Define interest rule option, application prompts user to define interest rules:

```
Please enter interest rules details in <Date> <RuleId> <Rate in %> format 
(or enter blank to go back to main menu):
>
```

User is then able to enter something like the following:
```
20230615 RULE03 2.20
```
Some constraints to note:
* Date should be in YYYYMMdd format
* RuleId is string, free format
* Interest rate should be greater than 0 and less than 100
* If there's any existing rules on the same day, the latest one is kept

Then system responds by listing all interest rules orderd by date:
(assuming there are already RULE01 and RULE02 in the system) 
```
Interest rules:
| Date     | RuleId | Rate (%) |
| 20230101 | RULE01 |     1.95 |
| 20230520 | RULE02 |     1.90 |
| 20230615 | RULE03 |     2.20 |

Is there anything else you'd like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

## Print Statement
Upon selecting Print statement option, application prompts user to select which account to print the statement for:

```
Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
>
```

When user enters the account
```
AC001 202306
```

System then responds with the following account statement, which shows all the transactions and interest for that month (transaction type for interest is I):
```
Account: AC001
| Date     | Txn Id      | Type | Amount | Balance |
| 20230601 | 20230601-01 | D    | 150.00 |  250.00 |
| 20230626 | 20230626-01 | W    |  20.00 |  230.00 |
| 20230626 | 20230626-02 | W    | 100.00 |  130.00 |
| 20230630 |             | I    |   0.39 |  130.39 |
```

How to apply the interest rule:
* Interest is applied on end of day balance
```
| Period              | Num of days | EOD Balance | Rate Id | Rate | Annualized Interest      |
| 20230601 - 20230614 | 14          | 250         | RULE02  | 1.90 | 250 * 1.90% * 14 = 66.50 |
| 20230615 - 20230625 | 11          | 250         | RULE03  | 2.20 | 250 * 2.20% * 11 = 60.50 |
| 20230626 - 20230630 |  5          | 130         | RULE03  | 2.20 | 130 * 2.20% *  5 = 14.30 |
(this table is provided to help you get an idea how the calculation is done, it should not be displayed in the output)
```
* Therefore total interest is: (66.50 + 60.50 + 14.30) / 365 = 0.3871 => 0.39
* The interest is credited at the last day of the month

## Quit
When user chooses to quit, user enters:
```
q
```

System responds with:
```
Thank you for banking with AwesomeGIC Bank.
Have a nice day!
```
    """
class BankingApp:
    def __init__(self):
        self.accounts={}
        #self.account = BankAccount("123456789") #TBD assign a new bank account number , list of bank accs ?
        self.interest_rules = {} #?????

    def run(self):
        print("Welcome to AwesomeGIC Bank! What would you like to do?")
        while True:
            print("[T] Input transactions")
            print("[I] Define interest rules")
            print("[P] Print statement")
            print("[Q] Quit")
            choice = input("> ").strip().upper()

            if choice == "T":
                self.input_transactions()
            elif choice == "I":
                self.define_interest_rules()
            elif choice == "P":
                self.print_statement()
            elif choice == "Q":
                print("Thank you for banking with AwesomeGIC Bank.")
                print("Have a nice day!")
                return
            else:
                print("Invalid choice. Please try again.")
            print("\nIs there anything else you'd like to do?")

    def input_transactions(self):
        #20230626 AC001 W 100.00
        print("Please enter transaction details in <Date> <Account> <Type> <Amount> format")
        print("or enter blank to go back to main menu): ")
        trn_details = input("> ").strip().upper()
        split_list=trn_details.split(" ")
        if len(split_list)>1:
            if len(split_list)==4:
                trn_date_str=split_list[0]
                bank_acc_num=split_list[1]
                trn_type=split_list[2]
                amount_str=split_list[3]
            else:
                print("Invalid Input Format! Please enter transaction details in <Date> <Account> <Type> <Amount> format (or enter blank to go back to main menu): ")
                return
        else:
            return

        '''
        * Date should be in YYYYMMdd format
        * Account is a string, free format
        * Type is D for deposit, W for withdrawal, case insensitive
        * Amount must be greater than zero, decimals are allowed up to 2 decimal places
        * An account's balance should not be less than 0. Therefore, the first transaction on an account should not be a withdrawal, and any transactions thereafter should not make balance go below 0
        * Each transaction should be given a unique id in YYYMMdd-xx format, where xx is a running number (see example below)
        '''
        #validation

        trn_date=utils.get_date(trn_date_str)
        if trn_date is None:
            print("Invalid date format. Please use YYYYMMdd format.")
            return
    
        amount=utils.get_number(amount_str)
        if amount is None:
            print("Amount is not a number. Please input a number up to 2 decimal places")
            return
        else:
            if amount <= 0:
                print("Amount must be greater than zero. Please re-enter.")
                return
            else:
                #up to 2 decimal places
                if not utils.is_two_decimal_places(amount_str):
                    print("Amount must be up to 2 decimal places. Please re-enter.")
                    return

        bank_acc=self.get_bank_acc(bank_acc_num)
        
        if trn_type == "D":
            if not bank_acc.add_transactions(trn_type, trn_date, amount):
                return
        elif trn_type == "W":
            if not bank_acc.add_transactions(trn_type, trn_date, amount):
                return
        else:
            print("Invalid transaction type. Please use these transaction types: D for deposit, W for withdrawal")
            return
        
        #add back
        self.accounts[bank_acc_num]=bank_acc

        #print statement
        self.print_statement_for_acc(bank_acc,print_balance=False)

    def define_interest_rules(self):
        #20230615 RULE03 2.20
        print("Please enter interest rules details in <Date> <RuleId> <Rate in %> format")
        print("or enter blank to go back to main menu):")
        interest_rule_details = input("> ").strip().upper()
        split_list=interest_rule_details.split(" ")
        logger.info(split_list)
        if len(split_list)>1:
            if len(split_list)==3:# TBD while loop
                interest_date_str=split_list[0]
                rule_id=split_list[1]
                rate_str=split_list[2]
            else:
                print("Invalid Input Format! Please enter interest rules details in <Date> <RuleId> <Rate in %> format):")
                return
        else:
            return

        #validation
        '''
        * Date should be in YYYYMMdd format
        * RuleId is string, free format
        * Interest rate should be greater than 0 and less than 100
        * If there's any existing rules on the same day, the latest one is kept
        '''        
        interest_date=utils.get_date(interest_date_str)
        if interest_date is None:
            print("Invalid date format. Please use YYYYMMdd format.")
            return

        rate=utils.get_number(rate_str)
        if rate is None:
            print("Amount is not a number. Please input a number up to 2 decimal places")
        else:
            if rate <= 0 or rate >=100 :
                print("Rate must be between 0 and 100. Please re-enter.")
                return
       
        interest_date_str=interest_date.strftime("%Y%m%d")
        self.interest_rules[interest_date_str]=(rule_id, rate)
        logger.debug(self.interest_rules)
        logger.info("Interest rule added successfully.")

        self.print_interest_rules()

    def print_interest_rules(self) -> None:
        print(f"Interest rules:")
        print("Date     | RuleId | Rate (%)")
        for date,interest_rule in self.interest_rules.items():
            rule_id, rate = interest_rule
            print(f"{date} | {rule_id:6} | {rate:7.2f}")

        print("\n")

    def print_statement(self) -> None:
        #AC001 202306
        print("Please enter account and month to generate the statement <Account> <Year><Month>")
        print("(or enter blank to go back to main menu):")
        print_details = input("> ").strip().upper()
        split_list=print_details.split(" ")
        logger.info(split_list)
        if len(split_list)>1:
            if len(split_list)==2:
                bank_acc_num=split_list[0]
                yyyymm=split_list[1]
            else:
                print("Invalid Input Format! Please enter account and month to generate the statement <Account> <Year><Month>")
                return
        else:
            return

        bank_acc=self.get_bank_acc(bank_acc_num)

        self.calculate_interest_for_acc(bank_acc,yyyymm)

        self.print_statement_for_acc(bank_acc, yyyymm=yyyymm)
    
    def print_statement_for_acc(self,bank_acc:BankAccount,
                                yyyymm:int=None,
                                print_balance:bool=True
                                ) -> None:
        bank_acc.print_statement(yyyymm, print_balance=print_balance)

    def get_bank_acc(self,bank_acc_num) -> BankAccount:
        bank_acc= self.accounts.get(bank_acc_num)
        if bank_acc is None:
            bank_acc=self.create_bank_acc(bank_acc_num)
        
        return bank_acc
    
    def create_bank_acc(self,bank_acc_num:str) -> BankAccount:
        return BankAccount(bank_acc_num)
    
    def calculate_interest_for_acc(self, bank_acc:BankAccount,yyyymm:int) -> float:
        acc_trns=bank_acc.get_transactions(yyyymm)
        month_first_day, month_last_day=utils.get_month_first_last_day(yyyymm)

        if not self.interest_rules:
            interest=0
        else:        
            # Find the most recent interest rule before the given date
            for date in sorted(self.interest_rules.keys()):
                rule,rate = self.interest_rules.get(date)
                #apply rule to all transactions from this date
                if rule[2] <= date:
                    applicable_rule = rule
                    break

            if applicable_rule:
                rate = applicable_rule[1]
                interest = self.balance * (rate / 100)
            
        bank_acc.add_transactions(trn_type="I", date=month_last_day, amount=interest)
        return interest
    