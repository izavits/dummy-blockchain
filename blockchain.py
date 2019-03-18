# Represent a blockchain
# A blockchain is an immutable, sequential chain of records, called blocks.
# They contain transactions, data, files, etc.
# They are chained together using hashes.

# Each new block contains within itself the hash of the previous block.
# This is crucial because this is what gives blockchains immutability.
# If an attacker corrupts an earlier block in the chain, then all subsequent
# blocks will contain incorrect hashes.

# When the blockchain is instantiated we will need to seed it with a genesis
# block. We will also need to add a "proof" to this block, which is the result
# of mining (proof of work).

# A Proof of Work (PoW) algorithm is how new blocks are created (or mined) on
# the blockchain. The goal of PoW is to discover a number which solves a problem.
# The number must be difficult to find but easy to verify.

import hashlib
import json
from time import time

class Blockchain(object):
    """
    This is the representation of the Blockchainself.
    """

    def __init__(self):
        """Constructor method"""
        self.chain=[]
        self.current_transactions=[]

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)


    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain.

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block={
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions (since we used them in the block)
        self.current_transactions=[]
        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction that will go to the next mined block.

        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block

        :param block: <dict> Block
        :return: <str>
        """
        block_string=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()



    @property
    def last_block(self):
        """Returns the last block in the chain"""
        return self.chain[-1]
