var Ipfs = artifacts.require("Ipfs");

module.exports = function(deployer) {
		  deployer.deploy(Ipfs);
};

