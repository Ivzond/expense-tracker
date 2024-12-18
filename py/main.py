import logging
from profile import runctx

import sber
import sovcom
import tinkoff
import vtb
from connect import session, SberTransaction, SovcomTransaction, TinkoffTransaction, VTBTransaction

from sqlalchemy.dialects.postgresql import insert

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s:%(funcName)s()',
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    transactions = {
        'sber': (sber.get_transactions(), SberTransaction),
        'sovcom': (sovcom.get_transactions(), SovcomTransaction),
        'tinkoff': (tinkoff.get_transactions(), TinkoffTransaction),
        'vtb': (vtb.get_transactions(), VTBTransaction)
    }

    for _, (source_transactions, TransactionClass) in transactions.items():
        for transaction in source_transactions:
            print(f"Inserting transaction: {transaction}")
            try:
                session.execute(insert(TransactionClass).values(transaction).on_conflict_do_nothing())
                session.commit()
            except Exception as e:
                session.rollback()

    session.close()