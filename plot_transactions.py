import matplotlib.pyplot as plt
import os
from datetime import timedelta


def plot_transactions(transactions: list, photo_save_path: str = None, file_save_path: str = None):
    """
    Plot the accumulated amounts of transactions over time.

    Parameters:
    transactions (list): A list of tuples containing the transaction date and amount.
    """
    if not transactions:
        print('No transactions found.')
        return
    total_balance = 0
    chart_data = []
    start_date = transactions[0][0]
    end_date = transactions[-1][0]
    current_date = start_date

    while current_date <= end_date:
        daily_total = 0
        for date, amount in transactions:
            if date == current_date:
                daily_total += amount
        total_balance += daily_total
        chart_data.append((current_date, total_balance))
        current_date += timedelta(days=1)

    # Create a sequence of dates that includes all dates between the start and end date of the transactions
    all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Create a list of accumulated amounts for all dates in the sequence
    accumulated_amounts = []
    balance = 0
    for date in all_dates:
        for transaction_date, transaction_amount in transactions:
            if transaction_date == date:
                balance += transaction_amount
        accumulated_amounts.append(balance)

    # Create the graph
    fig, ax = plt.subplots()
    ax.plot(all_dates, accumulated_amounts)
    ax.set_xticks([all_dates[i] for i in range(0, len(all_dates), 5)])
    ax.set_xticklabels([date.strftime('%d.%m.%y') for date in all_dates[::5]], rotation=90)
    ax.ticklabel_format(style='plain', axis='y')  # Add this line to disable scientific notation
    ax.set_xlabel('Date')
    ax.set_ylabel('Accumulated Amount')
    ax.grid(True)

    # Save the plot as a PNG file
    if photo_save_path:
        fig.tight_layout()
        fig.set_size_inches([8, 6])
        fig.savefig(photo_save_path, dpi=700, bbox_inches='tight')
        # if file will be more than allowed by telegram API
        if os.path.getsize(photo_save_path) > 512*1024:
            fig.savefig(photo_save_path, dpi=350, bbox_inches='tight')
    if file_save_path:
        fig.tight_layout()
        fig.set_size_inches([8, 6])
        fig.savefig(file_save_path, dpi=1400, bbox_inches='tight')