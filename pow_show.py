# pow_show.py
from flask import Blueprint, render_template
from Blockchain import Blockchain
from Block import Block
from timeit import default_timer as timer
import random
import string
import threading

# Blueprint for pow_show
pow_show_bp = Blueprint('pow_show', __name__)

# Store running time for each difficulty level
pow_results = {
    "random_nonce": [],
    "iterative_nonce": []
}

# Generates random string
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for _ in range(y))

# Add random transactions
def add_transaction(block, transactions_length):
    for _ in range(transactions_length):
        if random.random() > 0.9:
            block.add_t({
                "user": random_char(random.randint(5, 15)),
                "v_file": random_char(random.randint(5, 15)),
                "file_data": random_char(random.randint(10, 50)),
                "file_size": random.randint(100, 1000)
            })

# Main function to calculate PoW times
def calculate_pow_results():
    pow_results["random_nonce"].clear()
    pow_results["iterative_nonce"].clear()
    
    for difficulty in range(2, 6):
        Blockchain.difficulty = difficulty
        block_index = random.randint(0, 2000)
        transactions_length = random.randint(10, 20)

        # Create block and Blockchain
        block = Block(block_index, [], "0")
        blockchain = Blockchain()

        # Start a thread to add transactions in parallel
        transaction_thread = threading.Thread(target=add_transaction, args=(block, transactions_length))
        transaction_thread.start()
        transaction_thread.join()  # Wait for the transaction thread to finish

        # Measure time for first PoW algorithm
        start = timer()
        blockchain.p_o_w(block)
        end = timer()
        pow_results["random_nonce"].append({"difficulty": difficulty, "time": round(end - start, 5)})

        # Measure time for second PoW algorithm
        start = timer()
        blockchain.p_o_w_2(block)
        end = timer()
        pow_results["iterative_nonce"].append({"difficulty": difficulty, "time": round(end - start, 5)})

@pow_show_bp.route("/pow_show")
def pow_show():
    calculate_pow_results()
    return render_template("pow_show.html", pow_results=pow_results)
