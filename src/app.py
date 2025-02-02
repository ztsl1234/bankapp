import logging
from datetime import datetime

from banking_app import BankingApp

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = BankingApp()
    app.run()