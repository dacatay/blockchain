import hashlib
import json

from time import time
from uuid import uuid4

from flask import Flask

class Blockchain(object):

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.new_block(previous_hash=1, proof=100)   # create nemesis block

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block

        :param previous_hash: (optional) <str> Hash previous block
        :param proof: <str> proff as given by the proof of work algorithm
        :return: <dict> new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # reset current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        return block


    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block

        :param sender: <str> Adress of the Sender
        :param recipient: <str> Adress of the recipient
        :param amount: <int> Amount currency
        :return: <int> returns idnex of the block that holds this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] +1


    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 has of a block

        :param block: <dict> block
        :return: <str> hash string
        """

        # make sure that the dict is ordered, otherwise the hashes become inconsistent
        block_string = json.dumps(block, sort_key=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - find number p' such that hash(pp') contains leading 4 zeroes where p is the previous p'
         - p i the previous proof, and p' is the new proof

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: does hash/alst_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True if correct, False if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'


# Instantiate Flask node
app = Flask(__name__)

# generate globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# instantiate blockchain
blockchain = Blockchain()

@app.route('/mine', method=['GET'])






