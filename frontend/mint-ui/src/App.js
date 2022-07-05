import logo from './assets/images/logo-bg.png';
import './App.css';

import { loadWeb3, loadContract, connectWallet, shortenAddress, requestApprovalForTokenAsync } from './contracts';
import { useEffect, useState } from 'react';
import nftAbi from './contracts/abis/nft.json'
import busdAbi from './contracts/abis/busd.json'
import configs from './configs';
function App() {
  const [nftContract, setNftContract] = useState();
  const [currentBusd, setCurrentBUSD] = useState(null);
  const [allowance, setAllowance] = useState(0);
  const [ownedNfts, setOwnedNfts] = useState([]);
  const [busdContract, setBusdContract] = useState();
  const BASE_IMAGE_CID = "QmSD1Gx6uoF2mGK5jSGdQDbRrWthtM1V219iwYcYyPFzcL";
  const [connectedAccount, setConnectedAccount] = useState();
  const [mintAmount, setMintAmount] = useState(1);
  const [approveAmount, setApproveAmount] = useState(0);
  const [burningTokenIds, setBurningTokenIds] = useState(new Set());
  const START_BLOCK = 20442946;
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
    if (!busdContract || !nftContract || !connectedAccount)
      return;
    busdContract.methods.allowance(connectedAccount, nftContract._address)
      .call()
      .then(async (result) => {
        setAllowance(parseInt(result));
      })

  }, [connectedAccount, busdContract, nftContract])

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
  //   async function loadImgURL(cid, mime, limit) {
  //     if (cid == "" || cid == null || cid == undefined) {
  //         return;
  //     }
  //     for await (const file of ipfs.get(cid)) {
  //         if (file.size > limit) {
  //             return;
  //         }
  //         const content = [];
  //         if (file.content) {
  //             for await(const chunk of file.content) {
  //                 content.push(chunk);
  //             }
  //             return URL.createObjectURL(new Blob(content, {type: mime}));
  //         }
  //     }
  // }

  const fetchOwnNfts = async (ownerAddress) => {
    nftContract.getPastEvents('Transfer', {
      filter: { to: ownerAddress },
      fromBlock: START_BLOCK,
      toBlock: 'latest'
    })
      .then(async (transferEvents) => {
        nftContract.getPastEvents('NftBurned', {
          filter: { owner: ownerAddress },
          fromBlock: START_BLOCK,
          toBlock: 'latest'
        })
          .then(async (burnedEvents) => {
            let transferNfts = transferEvents.map((event) => {
              const { returnValues } = event;
              const { tokenId } = returnValues;
              return { tokenId: tokenId };
            })
            let burnedNfts = burnedEvents.map((event) => {
              const { returnValues } = event;
              const { tokenId } = returnValues;
              return { tokenId: tokenId };
            })

            let burnedFlatten = burnedNfts.map(({ tokenId }) => tokenId);
            console.log(burnedFlatten, burnedNfts)
            let nfts = transferNfts.filter(transferNft => !burnedFlatten.includes(transferNft.tokenId));
            // setOwnedNfts([...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts]);
            setOwnedNfts(nfts);
          })

      });
  }

  const onRequestApproval = async () => {

    await requestApprovalForTokenAsync(busdContract, nftContract._address, connectedAccount, (approveAmount * 100000000 * 10000000000).toString());
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

    console.log(checked, burningTokenIds)
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
        // NotificationManager.success(`Mint successfully.`);
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
          <img src={logo} className="App-logo" alt="logo" />

        </a>
        <p>
          Mint page template
        </p>
      </header>
      <main>
        <br />
        {connectedAccount
          ? (<>
            <p>Contract: {shortenAddress(nftContract?._address)}</p>
            <p>Connected wallet: {shortenAddress(connectedAccount)}</p>
            <p>Current Balance: {currentBusd}</p>
            <br />
            {allowance <= 0
              ?
              <div>
                <input type={"number"} onChange={e => { setApproveAmount(e.target.value) }} placeholder="input number" defaultValue={1} min={1} />
                <button onClick={onRequestApproval}>Request Approval</button>
              </div>
              : <span style={{ color: "white" }}>Approved: {allowance}</span>}

            <br />
            <div>
              <input type={"number"} onChange={e => { setMintAmount(e.target.value) }} placeholder="input number" defaultValue={1} min={1} />
              <button onClick={onMint}>Mint</button>
            </div>
            <br />
            <div>
              {/* <input type={"number"} onChange={e => { setMintAmount(e.target.value) }} placeholder="input number" defaultValue={1} min={1} /> */}
              <span style={{ color: "white" }}>{Array.from(burningTokenIds).join(", ")}</span>
              {burningTokenIds.size > 0 ? <button onClick={onBurnMultiple}>Burn many</button> : <span style={{ color: "white" }}>Nothing to burn</span>}

            </div>
            <br />
            {ownedNfts ? <>
              <div className='nfts'>
                {ownedNfts.map(({ tokenId }) =>
                  <div className='nft-item' key={`own-token-${tokenId}`}>
                    <input type={"checkbox"} onChange={(e) => onCheckboxChange(e, tokenId)} />
                    <img src={`https://ipfs.io/ipfs/${BASE_IMAGE_CID}/${tokenId}.png`} alt={tokenId} />
                    <button onClick={(e) => onBurn(tokenId)}>Burn</button>
                  </div>)
                }
              </div>

            </> : <></>}
          </>
          )
          : <button onClick={onConnectWallet}>Connect wallet</button>}

      </main>
      <footer>

      </footer>
    </div>
  );
}

export default App;
