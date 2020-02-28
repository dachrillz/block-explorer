"""Retrieve blocks in raw hex format

Returns:
    [type] -- [description]
"""

import requests

LATESTBLOCK = r"https://blockchain.info/latestblock"
RAWBLOCK = r"https://blockchain.info/block/"
FORMAT = r"?format=hex"

def get_block_string(blockhash):
    """Formats blockhash into blockchain.info query string
    Arguments:
        blockhash {[type]} -- [description]
    Returns:
        [type] -- [description]
    """
    return f"{RAWBLOCK}{blockhash}{FORMAT}"

def latest_block_as_raw():
    """Get latest known block in blockchain as HEX
    Raises:
        Exception: If get latest block query fails -> throws excpetion
        Exception: If can not retrieve raw block fails -> throws exception
    Returns:
        [type] -- [description]
    """

    # Get latest block hash
    latest_block = requests.get(LATESTBLOCK)

    if not latest_block.ok:
        raise Exception(latest_block.reason)
    print(f"Latest block response ok? -> {latest_block.ok}")

    latest_block_as_json = latest_block.json()
    print(f"Hash of latest block : {latest_block_as_json['hash']}")

    FOR_TEST = '0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103';

    #latest_block_url = get_block_string(latest_block_as_json['hash'])
    latest_block_url = get_block_string(FOR_TEST)

    raw_block = requests.get(latest_block_url)
    if not raw_block.ok:
        raise Exception(raw_block.reason)
    print(f"Raw block response ok? -> {raw_block.ok}")
    print(raw_block.text)
    return raw_block.raw

latest_block_as_raw()
