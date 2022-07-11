import logo from './assets/images/logo-bg.png';
import './App.css';

import { loadWeb3, loadContract, connectWallet, shortenAddress, requestApprovalForTokenAsync } from './contracts';
import { useEffect, useState } from 'react';
import nftAbi from './contracts/abis/nft.json'
import busdAbi from './contracts/abis/erc20.json'
import configs from './configs';
function App() {
  const [nftContract, setNftContract] = useState();
  const [currentBusd, setCurrentBUSD] = useState(null);
  // const [allowance, setAllowance] = useState(0);
  const [ownedNfts, setOwnedNfts] = useState([]);
  const [busdContract, setBusdContract] = useState();
  const BASE_IMAGE_CID = "QmSD1Gx6uoF2mGK5jSGdQDbRrWthtM1V219iwYcYyPFzcL";
  const [connectedAccount, setConnectedAccount] = useState();
  const [mintAmount, setMintAmount] = useState(1);
  // const [approveAmount, setApproveAmount] = useState(0);
  const [burningTokenIds, setBurningTokenIds] = useState(new Set());
  // const START_BLOCK = 20442946;
  const { nftContractAddress, busdContractAddress } = configs;
  const changeAccount = (accounts) => {
    if (accounts && accounts.length > 0) {
      setConnectedAccount(accounts[0]);
      fetchOwnNfts(accounts[0])
    } else {
      setConnectedAccount(null);
    }
  }

  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        changeAccount(accounts);
      }
    })

  })
  useEffect(() => {
    const contractAddress = busdContractAddress;
    loadContract(busdAbi, contractAddress, {
      onContractInit: (contract) => {

        setBusdContract(contract)

      }
    });
  }, [busdContractAddress])


  useEffect(() => {
    const contractAddress = nftContractAddress;
    loadContract(nftAbi, contractAddress, {
      onContractInit: (contract) => {

        setNftContract(contract)

      }
    });
  }, [nftContractAddress])

  useEffect(() => {
    if (busdContract == null || connectedAccount == null)
      return;
    busdContract.methods.balanceOf(connectedAccount).call().then(result => {
      setCurrentBUSD(result);
    })
  }, [busdContract, connectedAccount])

  const onConnectWallet = async (e) => {
    await connectWallet({
      onAccountConnected: (accounts) => {
        changeAccount(accounts);
      },
      onNetworkChanged: (networkId) => {

      }
    })
  }


  const onRequestApproval = async () => {
    const approveAmount = window.web3.utils.toWei("100000000000000", "ether");
    // console.log(approveAmount)
    await requestApprovalForTokenAsync(busdContract, nftContract._address, connectedAccount, approveAmount.toString());
  }

  const fetchOwnNfts = (connectedAccount) => {
    nftContract.methods.tokensOfOwner("0x609e505827cbabf618a08c58c3a36589888f18ba").call().then(rs => {
      console.log(rs)
      setOwnedNfts(rs);
    })

  }

  const onMint = async (e) => {

    nftContract.methods
      .safeMint(mintAmount)
      .send({ from: connectedAccount })
      .then(result => {
        // NotificationManager.success(`Mint successfully.`);
        fetchOwnNfts(connectedAccount)
      })
      .catch(error => {
        // NotificationManager.error(`Mint failed.`);
        console.error(error)

      });
  }
  const onCheckboxChange = ({ target }, tokenId) => {
    const { checked } = target;

    if (burningTokenIds) {
      if (checked) {
        burningTokenIds.add(tokenId)
      } else {
        burningTokenIds.delete(tokenId)
      }
    }


    setBurningTokenIds(burningTokenIds ? new Set(burningTokenIds) : new Set());
  }
  const onBurn = (tokenId) => {
    nftContract.methods
      .burn(tokenId)
      .send({ from: connectedAccount })
      .then(result => {
        // // NotificationManager.success(`Mint successfully.`);
        fetchOwnNfts(connectedAccount)
      })
      .catch(error => {
        // NotificationManager.error(`Mint failed.`);
        console.error(error)

      });
  }

  const onBurnMultiple = () => {
    console.log(burningTokenIds)
    if (burningTokenIds.size <= 0)
      alert("Invlid tokens");
    nftContract.methods
      .burnBatch(Array.from(burningTokenIds))
      .send({ from: connectedAccount })
      .then(result => {
        // NotificationManager.success(`Mint successfully.`);
        fetchOwnNfts(connectedAccount)
      })
      .catch(error => {
        // NotificationManager.error(`Mint failed.`);
        console.error(error)

      });
  }

  return (
    <div className="App">
      <header className="App-header">
        <a
          className="App-link"
          href="https://quano6.com"
          target="_blank"
          rel="noopener noreferrer"
        >

        </a>
        <p>
          Minting page
        </p>
      </header>
      <main>
        <br />
        {connectedAccount
          ? (<>
            {/* <p>Contract: {shortenAddress(nftContract?._address)}</p> */}
            <p>Connected wallet: {shortenAddress(connectedAccount)}</p>
            <p>Current Balance: {currentBusd}</p>
            <br />
            {/* {allowance <= 0
              ?
              <div>
                <input type={"number"} onChange={e => { setApproveAmount(e.target.value) }} placeholder="input number" defaultValue={1} min={1} />
                <button onClick={onRequestApproval}>Request Approval</button>
              </div>
              : <span style={{ color: "white" }}>Approved: {allowance}</span>} */}
            <button onClick={onRequestApproval}>Request Approval</button>
            <br />
            <div>
              <input type={"number"} onChange={e => { setMintAmount(e.target.value) }} placeholder="input number" defaultValue={1} min={1} />
              <button onClick={onMint}>Mint</button>
            </div>
            <br />
            {/* <div>
              <span>{Array.from(burningTokenIds).join(", ")}</span>
              {burningTokenIds.size > 0 ? <button onClick={onBurnMultiple}>Burn many</button> : <span >Nothing to burn</span>}

            </div> */}
            <br />
            {ownedNfts ? <>
              <div className='nfts'>
                {ownedNfts.map((tokenId) =>
                  <div className='nft-item' key={`own-token-${tokenId}`}>
                    {/* <input type={"checkbox"} onChange={(e) => onCheckboxChange(e, tokenId)} /> */}
                    <span style={{ right: "0", top: "0", position: "absolute" }}>#{tokenId}</span>
                    <img src={`https://wicked.mypinata.cloud/ipfs/${BASE_IMAGE_CID}/${tokenId}.png`} alt={tokenId} />
                    {/* <button onClick={(e) => onBurn(tokenId)}>Burn</button> */}
                  </div>)
                }
              </div>

            </> : <></>}
          </>
          )
          : <button onClick={onConnectWallet}>Connect wallet</button>}

      </main>
      <footer>
        by quano6
      </footer>
    </div>
  );
}

export default App;
