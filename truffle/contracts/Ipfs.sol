pragma solidity >= 0.5.0 < 0.7.0;

contract Ipfs {
	mapping (string => string) hashes;

    function addHash(string memory id, string memory hash) public {
        hashes[id] = hash;
    }

    function getHash(string memory id) public view returns (string memory x) {
    	return hashes[id];
    }
}
