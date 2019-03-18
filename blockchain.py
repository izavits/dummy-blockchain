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

# The whole point of blockchains is that they should be decentralized.
# Being decentralized though, they all should reflect the same chain. This is the
# problem of Consensus.


import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
from flask import Flask
from flask import jsonify
from flask import request
from urllib2 import urlparse
import requests
from pow import valid_proof
from pow import proof_of_work

class Blockchain(object):
    """
    This is the representation of the Blockchainself.
    """

    def __init__(self):
        """Constructor method"""
        self.chain=[]
        self.current_transactions=[]
        self.nodes=set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)


    def register_node(self, address):
        """
        Add a new network node to the set of nodes

        :param address: <str> Address of node. Eg. 'http://127.0.0.1:5000'
        :return: None
        """
        parsed_url=urlparse.urlparse(address)
        self.nodes.add(parsed_url.netloc)

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


    def valid_chain(self, chain):
        """
        Determine if the given chain is valid.

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """
        last_block=chain[0]
        current_index=1
        while current_index<len(chain):
            block=chain[current_index]
            print(last_block)
            print(block)
            print("\n----------\n")
            # Check the hash of the block
            if block['previous_hash']!=self.hash(last_block):
                return False
            # Check the Proof of Work
            if not valid_proof(last_block['proof'], block['proof']):
                return False
            last_block=block
            current_index+=1

        return True


    def resolve_conflicts(self):
        """
        This is actually the Consensus algorithm. It resolves conflicts by replacing
        the chain with the longest one in the network.

        :return: <bool> True if our chain was replaced, False if not
        """
        neighbours=self.nodes
        new_chain=None
        # We just look for chains longer than the current one
        max_length=len(self.chain)
        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response=requests.get('http://'+node+'/chain')
            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']
                # Check if the length is longer and the chain is valid
                if length>max_length and self.valid_chain(chain):
                    max_length=length
                    new_chain=chain

        # Replace the chain if we found a new valid one
        if new_chain:
            self.chain=new_chain
            return True

        return False



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


# Instantiate the Node in the network
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Run the PoW algorithm to mine a new block
    last_block=blockchain.last_block
    last_proof=last_block['proof']
    proof=proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    # Forge the new Block by adding it to the chain
    previous_hash=blockchain.hash(last_block)
    block=blockchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values=request.get_json()
    # Check that the required fields are in the POST data
    required=['sender', 'recipient', 'amount']
    if values is None:
        res={'message':'Missing data'}
        return jsonify(res), 400
    for r in required:
        if not r in values:
            res={'message':'Missing data'}
            return jsonify(res), 400
    # Create the new transaction
    index=blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response={'message': 'Transaction will be added to Block '+str(index)}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values=request.get_json()
    nodes=values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response={
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced=blockchain.resolve_conflicts()

    if replaced:
        response={
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response={
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
