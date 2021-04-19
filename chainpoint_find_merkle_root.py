import requests
from requests import ConnectionError
import re
import json



def verify_proofs(proof,version_chainpoint="1"):
    """verify proofs
    param version_chainpoint:string like "1.x" or
     "2.x" or integer like 1 or 2. (3 is not implemented)"""
    try:
        proof = json.loads(proof)
    except TypeError:
        pass
    
    version_chainpoint = int(str(version_chainpoint)[0])
    assert version_chainpoint in (1,2)
    
    if version_chainpoint == 1:
        tx_id = proof["header"]["tx_id"]
        merkle_root = proof["header"]["merkle_root"]
    else:
        tx_id = proof["targetHash"]
        merkle_root = proof["merkleRoot"]
    try:
        site = requests.get(f"https://www.blockchain.com/btc/tx/{tx_id}", timeout=3)
    except ConnectionError:
        return {"error": "network_error"}
    pattern = re.compile(r'(<span class="sc-1ryi78w-0 cILyoi sc-16b9dsl-1'+ \
                         ' ZwupP u3ufsr-0 eQTRKC" opacity="1">)([a-f0-9]{64})(</span>)')
    for i in pattern.findall(site.text):
        if i[1] != tx_id:
            return i[1]==merkle_root
    return None
