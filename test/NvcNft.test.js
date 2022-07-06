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

const ETHER = BigNumber.from(1000000000000000000n);
const PRICE = ETHER;
const COLLECTION_SIZE = 10000;
const BUSD_CONTRACT = "0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7";
const ADDRESS_RECEIVER = "0xE515BA407b97B053F89c4eecb8886F4C6101d4A3";
const BASE_URI = "ipfs://QmbksLtdi1yDJdHcPgVBc5cLyGGs5j4rMq4a4WXFFZu2XG/";
const NAME = "Next Venture Capital";
const SYMBOL = "NVC";

const createTestSuite =
  ({ contract, constructorArgs }) =>
  () => {
    context(`${contract}`, () => {
      beforeEach(async () => {
        const [addr1, addr2, addr3, addr4] = await ethers.getSigners();
        this.addr1 = addr1;
        this.addr2 = addr2;
        this.addr3 = addr3;
        this.addr4 = addr4;
        this.erc20 = await deployContract("BEP20Token", []);
        this.erc721 = await deployContract(contract, [this.erc20.address]);

        await this.erc20.approve(this.erc721.address, ETHER);
      });

      describe("Test Price", async () => {
        it("correct Price", async () => {
          expect(await this.erc721.PRICE()).to.eq(PRICE);
        });
      });

      describe("Test Collection Size", async () => {
        it("correct Collection Size", async () => {
          expect(await this.erc721.COLLECTION_SIZE()).to.eq(COLLECTION_SIZE);
        });
      });

      describe("Test BUSD_CONTRACT", async () => {
        it("correct BUSD_CONTRACT", async () => {
          expect(await this.erc721.BUSD_CONTRACT()).to.eq(BUSD_CONTRACT);
        });
      });

      describe("TEST ADDRESS_RECEIVER", async () => {
        it("correct ADDRESS_RECEIVER", async () => {
          expect(await this.erc721.ADDRESS_RECEIVER()).to.eq(ADDRESS_RECEIVER);
        });
      });

      describe("Test BASE_URI", async () => {
        it("correct BASE_URI", async () => {
          expect(await this.erc721.baseURI()).to.eq(BASE_URI);
        });
      });

      describe("Test totalSupply after minted", async () => {
        it("correct totalSupply after minted", async () => {
          await this.erc20.connect(this.addr4).mint(ETHER);
          await this.erc20
            .connect(this.addr4)
            .approve(this.erc721.address, ETHER);
          expect(
            parseInt(
              await this.erc20.connect(this.addr4).balanceOf(this.addr4.address)
            )
          ).to.greaterThan(0);
          const i = 1;
          let currentIndex = await this.erc721.totalSupply();
          await this.erc721.connect(this.addr4).safeMint(i);
          expect(await this.erc721.totalSupply()).to.eq(currentIndex + i);
        });
      });

      describe("Test totalSupply after burned", async () => {
        it("correct totalSupply after burned", async () => {
          await this.erc20
            .connect(this.addr4)
            .mint((ETHER * BigNumber.from(10n)).toString());
          await this.erc20
            .connect(this.addr4)
            .approve(
              this.erc721.address,
              (ETHER * BigNumber.from(10n)).toString()
            );
          expect(
            parseInt(
              await this.erc20.connect(this.addr4).balanceOf(this.addr4.address)
            )
          ).to.greaterThan(0);
          const mintAmount = 10;
          const burnArray = [4, 5, 6];
          await this.erc721.connect(this.addr4).safeMint(mintAmount);
          let currentIndex = await this.erc721.totalSupply();
          await this.erc721.connect(this.addr4).burnBatch(burnArray);
          expect(await this.erc721.totalSupply()).to.eq(currentIndex - 3);
          expect(this.erc721.connect(this.addr4).ownerOf(4)).to.be.revertedWith(
            "OwnerQueryForNonexistentToken"
          );
          expect(this.erc721.connect(this.addr4).ownerOf(5)).to.be.revertedWith(
            "OwnerQueryForNonexistentToken"
          );
          expect(this.erc721.connect(this.addr4).ownerOf(6)).to.be.revertedWith(
            "OwnerQueryForNonexistentToken"
          );
        });
      });

      describe("Test totalBurned", async () => {
        it("correct totalBurned", async () => {
          await this.erc20
            .connect(this.addr4)
            .mint((ETHER * BigNumber.from(10n)).toString());
          await this.erc20
            .connect(this.addr4)
            .approve(
              this.erc721.address,
              (ETHER * BigNumber.from(10n)).toString()
            );
          expect(
            parseInt(
              await this.erc20.connect(this.addr4).balanceOf(this.addr4.address)
            )
          ).to.greaterThan(0);
          const mintAmount = 10;
          const burnArray = [1, 2, 3];
          await this.erc721.connect(this.addr4).safeMint(mintAmount);
          let currentIndex = await this.erc721.totalBurned();
          await this.erc721.connect(this.addr4).burnBatch(burnArray);
          expect(await this.erc721.totalBurned()).to.eq(currentIndex + 3);
        });
      });

      describe("Test Name", async () => {
        it("correct Name", async () => {
          expect(await this.erc721.name()).to.eq(NAME);
        });
      });

      describe("Test Symbol", async () => {
        it("correct Symbol", async () => {
          expect(await this.erc721.symbol()).to.eq(SYMBOL);
        });
      });

      describe("Test safeMint", async () => {
        it("correct safeMint", async () => {
          await this.erc20.connect(this.addr4).mint(ETHER);
          await this.erc20
            .connect(this.addr4)
            .approve(this.erc721.address, ETHER);
          expect(
            parseInt(
              await this.erc20.connect(this.addr4).balanceOf(this.addr4.address)
            )
          ).to.greaterThan(0);
          const i = 1;
          let currentIndex = parseInt(await this.erc721.totalSupply());
          await this.erc721.connect(this.addr4).safeMint(i);
          expect(await this.erc721.totalMinted()).to.eq(currentIndex + i);
        });
      });
    });
  };

describe(
  "NvcNft",
  createTestSuite({
    contract: "NVCNFT",
    constructorArgs: [],
  })
);
