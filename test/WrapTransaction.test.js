const {
  deployContract,
  // getBlockTimestamp,
  // mineBlockTimestamp,
  // offsettedIndex,
} = require("./helpers.js");
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { BigNumber } = require("ethers");
const { constants } = require("@openzeppelin/test-helpers");
const { ZERO_ADDRESS } = constants;

const RECEIVER_MAGIC_VALUE = "0x150b7a02";
const GAS_MAGIC_VALUE = 20000;
const BUSD_CONTRACT = "0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7";

const createTestSuite =
  ({ contract, constructorArgs }) =>
  () => {
    context(`${contract}`, () => {
      beforeEach(async () => {
        this.contract = await deployContract(contract, []);
      });

      describe("BUSD_CONTRACT", async () => {
        it("correct BUSD_CONTRACT", async () => {
          expect(await this.contract.BUSD_CONTRACT()).to.eq(BUSD_CONTRACT);
        });
      });

      describe("correct BUSD_CONTRACT", async () => {
        it("correct BUSD_CONTRACT", async () => {
          expect(await this.contract.BUSD_CONTRACT()).to.eq(BUSD_CONTRACT);
        });
      });
    });
  };

describe(
  "WrapTransaction",
  createTestSuite({
    contract: "WrapTransactions",
    constructorArgs: [],
  })
);
