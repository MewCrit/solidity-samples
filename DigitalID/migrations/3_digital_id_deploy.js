const DigitalID = artifacts.require("DigitalID");

module.exports = async function(deployer) {
	await deployer.deploy(DigitalID)
};