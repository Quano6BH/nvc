// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// When running the script with `npx hardhat run <script>` you'll find the Hardhat
// Runtime Environment's members available in the global scope.
const hre = require("hardhat");

async function main() {
  // Hardhat always runs the compile task when running scripts with its command
  // line interface.
  //
  // If this script is run directly using `node` you may want to call compile
  // manually to make sure everything is compiled
  // await hre.run('compile');

  // We get the contract to deploy
  // const erc20ContractFactory = await hre.ethers.getContractFactory("NVCNFT");
  // const erc20Contract= await nftContractFactory.deploy();
  const busdAddress = "0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7";
  const nftContractFactory = await hre.ethers.getContractFactory("NVCNFT");
  const nftContract = await nftContractFactory.deploy(busdAddress);

  const wrapContractFactory = await hre.ethers.getContractFactory(
    "WrapTransactions"
  );
  const wrapContract = await wrapContractFactory.deploy(busdAddress);

  await nftContract.deployed();
  console.log("nftContract deployed to:", nftContract.address);

  await wrapContract.deployed();
  console.log("wrapContract deployed to:", wrapContract.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
