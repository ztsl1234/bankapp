from datetime import datetime
import logging

from utils import utils

logger = logging.getLogger(__name__)


class BankAccount:
    def __init__(self, account_number):
        self.account_number = account_number
        self.balance = 0.0
        self.transactions = {}
        self.monthly_trn_dates = {}

    def add_transactions(self, trn_type:str, date, amount:float) -> bool:
        if trn_type=="W":
            if amount > self.balance:
                logger.error("Insufficient funds for withdrawal.")
                return False
            else:
                self.balance -= amount
        else:
            self.balance += amount
        date_str=date.strftime("%Y%m%d")
        yyyymm=date.strftime("%Y%m")

        trn_list=self.transactions.get(date)
        trn_list=[] if trn_list is None else trn_list

        trn_id="" if trn_type=="I" else f"{date_str}-{len(trn_list)+1:02}"
        trn_list.append((date_str,trn_id, trn_type, amount, self.balance))
        self.transactions[date]=trn_list

        mth_trn_dates=self.monthly_trn_dates.get(yyyymm)
        mth_trn_dates=[] if mth_trn_dates is None else mth_trn_dates

        mth_trn_dates.append(date)
        self.monthly_trn_dates[yyyymm]=mth_trn_dates
        return True
    
    def print_statement(self, yyyymm:int=None, print_balance:bool=True):
        
        tran_dict = self.transactions if yyyymm is None else self.get_transactions(yyyymm)
       
        print(f"Account: {self.account_number}")
        balance_heading="| Balance"
        if not print_balance:
            balance_heading=""

        print(f"Date     | Txn Id      | Type | Amount  {balance_heading}")

        #sort the transactions by date
        for date in sorted(tran_dict.keys()):
            trn_list = tran_dict.get(date)
            for trn in trn_list:
                date, trn_id, trn_type, amount, balance = trn
                balance_str=f"| {balance:7.2f}"
    
                if not print_balance:
                    balance_str=""

                print(f"{date} | {trn_id:11} | {trn_type:4} | {amount:7.2f} {balance_str}")
        
        #print("\n")

    def get_transactions(self, yyyymm:int) -> dict:
        mth_trn_dates=self.monthly_trn_dates.get(yyyymm)
        mth_trn_dates=[] if mth_trn_dates is None else mth_trn_dates
            
        tran_dict={}
        for date in mth_trn_dates:
            tran_dict[date]=self.transactions.get(date)
        return tran_dict
  