import re
from datetime import datetime


def read_transactions(filename: str) -> list:
    """
    Read the transactions from a file.

    Parameters:
    filename (str): The name of the file to read the transactions from.

    Returns:
    list: A list of tuples containing the transaction date and amount.
    """
    transactions = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = re.split(" [-+] ", line)
            if len(parts) != 2:
                continue
            date_str = parts[0]
            amount_str = parts[1].split('₸')[0].replace(' ', '').replace(',', '.')
            try:
                date = datetime.strptime(date_str, "%d.%m.%y").date()
                if ' + ' in line:
                    amount = float(amount_str)
                if ' - ' in line:
                    amount = float(amount_str) * -1
            except (ValueError, TypeError):
                continue
            transactions.append((date, amount))
    transactions.sort(key=lambda t: t[0])
    return transactions
