# Represent a blockchain
# A blockchain is an immutable, sequential chain of records, called blocks.
# They contain transactions, data, files, etc.
# They are chained together using hashes.

# Each new block contains within itself the hash of the previous block.
# This is crucial because this is what gives blockchains immutability.
# If an attacker corrupts an earlier block in the chain, then all subsequent
# blocks will contain incorrect hashes.

class Blockchain(object):
    """
    This is the representation of the Blockchainself.
    """

    def __init__(self):
        """Constructor method"""
        self.chain=[]
        self.current_transactions=[]

    def new_block(self):
        """Creates a new block and adds it to the chain"""
        pass

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
        """Hashes a block"""
        pass

    @property
    def last_block(self):
        """Returns the last block in the chain"""
        pass
