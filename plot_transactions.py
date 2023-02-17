import tkinter as tk
from datetime import timedelta
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_transactions(transactions: list, save_path: str = None):
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

    print('Total balance:', int(total_balance), '₸')

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

    # Create a tkinter window and add the graph to it
    root = tk.Tk()
    root.title('Transaction History')
    root.geometry('1024x768')

    # Create a style for the ttk widgets
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='white')
    style.configure('TLabel', background='white')
    style.configure('TButton', background='#4CAF50', foreground='white')

    # Create a frame to hold the graph
    graph_frame = ttk.Frame(root, padding=10)
    graph_frame.pack(fill='both', expand=True)

    # Create a canvas to hold the graph
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    # # Add a button to close the window
    # close_button = ttk.Button(root, text='Close', command=root.destroy)
    # close_button.pack(side='bottom', pady=10)
    # # Start the tkinter main loop
    # root.mainloop()

    # Optionally save the plot as a PNG file
    if save_path:
        fig.tight_layout()
        fig.set_size_inches([8, 6])
        fig.savefig(save_path, dpi=600, bbox_inches='tight')
