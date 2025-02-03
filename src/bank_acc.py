from datetime import datetime
import logging

from utils import utils
from transaction import Transaction

logger = logging.getLogger(__name__)

class BankAccount:

    def __init__(self, account_number:str):
        """
        Constructor

        Args:
            account_number (str): bank account number
        """
        self.account_number = account_number
        self.balance = 0.0
        self.transactions = {}
        self.monthly_trn_dates = {}

    def add_transaction(self, trn_type:str, trn_date, amount:float) -> bool:
        """
        Add a transaction to the transaction list for a bank account

        Args:
            trn_type (str): Transaction Type
            date (_type_): Transaction Date
            amount (float): Transaction Amount

        Returns:
            bool: _description_
        """
        if trn_type=="W":
            if amount > self.balance:
                print("Insufficient funds for withdrawal.")
                return False
            else:
                self.balance -= amount
        else:
            self.balance += amount
        date_str=trn_date.strftime("%Y%m%d")
        yyyymm=trn_date.strftime("%Y%m")

        trn_list=self.transactions.get(trn_date)
        trn_list=[] if trn_list is None else trn_list

        trn_id="" if trn_type=="I" else f"{date_str}-{len(trn_list)+1:02}"
        trn_list.append(Transaction(trn_date,trn_id, trn_type, amount, self.balance))
        self.transactions[trn_date]=trn_list

        mth_trn_dates=self.monthly_trn_dates.get(yyyymm)
        mth_trn_dates=[] if mth_trn_dates is None else mth_trn_dates

        mth_trn_dates.append(trn_date)
        self.monthly_trn_dates[yyyymm]=mth_trn_dates
        return True
    
    def print_statement(self, yyyymm:int=None, print_balance:bool=True):
        """
        print transactions

        Args:
            yyyymm (int, optional): Year Month. Defaults to None.
            print_balance (bool, optional): flag to display balance or not display. Defaults to True.
        """
        
        tran_dict = self.transactions if yyyymm is None else self.get_transactions(yyyymm)
       
        print(f"Account: {self.account_number}")
        balance_heading="| Balance"
        if not print_balance:
            balance_heading=""

        print(f"Date     | Txn Id      | Type | Amount  {balance_heading}")

        #sort the transactions by date
        for date in sorted(tran_dict.keys()):
            trn_list = tran_dict.get(date)
            for trn_obj in trn_list:
                trn_obj.print(print_balance)

    def get_transactions(self, yyyymm:int) -> dict:
        """
        Get the transactions for a Year Month

        Args:
            yyyymm (int): Year Month

        Returns:
            dict: map of transaction dates to list of transaction objects for each transaction dates
        """
        mth_trn_dates=self.monthly_trn_dates.get(yyyymm)
        mth_trn_dates=[] if mth_trn_dates is None else mth_trn_dates
            
        tran_dict={}
        for date in mth_trn_dates:
            tran_dict[date]=self.transactions.get(date)
        return tran_dict
