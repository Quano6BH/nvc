import logo from './assets/images/logo-bg.png';
import './App.css';

import { loadWeb3, loadContract, connectWallet, shortenAddress } from './contracts';
import { useEffect, useState } from 'react';
import nftAbi from './contracts/abis/nft.json'
function App() {
  const [nftContract, setNftContract] = useState();
  const [ownedNfts, setOwnedNfts] = useState([]);
  const BASE_IMAGE_CID = "QmSD1Gx6uoF2mGK5jSGdQDbRrWthtM1V219iwYcYyPFzcL";
  const [connectedAccount, setConnectedAccount] = useState();
  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        changeAccount(accounts);
      }
    })

  }, [connectedAccount])
  useEffect(() => {
    const contractAddress = "0xa7e36cbe8c97d9fb48dbf5587fd7e78cf13e552e";
    loadContract(nftAbi, contractAddress, {
      onContractInit: (contract) => {

        setNftContract(contract)

      }
    });
  }, [nftAbi])
  const changeAccount = (accounts)=>{
    if (accounts && accounts.length > 0) {
      setConnectedAccount(accounts[0]);
      fetchOwnNfts(accounts[0]);
    } else {
      setConnectedAccount(null);
    }
  }
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
      filter: { from: '0x0000000000000000000000000000000000000000', to: ownerAddress },
      fromBlock: 0,
      toBlock: 'latest'
    })
      .then(async (events) => {
        let nfts = events.map((event) => {
          const { returnValues } = event;
          const { tokenId } = returnValues;
          return { tokenId: tokenId };
        })
        // setOwnedNfts([...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts]);
        setOwnedNfts(nfts);
      });
  }
  const onMint = async (e) => {
    nftContract.methods
      .mintToMultiple(connectedAccount, 1)
      .send({ from: connectedAccount })
      .then(result => {
        // NotificationManager.success(`Mint successfully.`);
        console.log(result)
      })
      .catch(error => {
        // NotificationManager.error(`Mint failed.`);
        console.error(error)

      });
  }
  const onBurn = (tokenId) => {

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
        <br/>
        {connectedAccount
          ? (<>
            <p>Contract: {shortenAddress(nftContract?._address)}</p>
            <p>Connected wallet: {shortenAddress(connectedAccount)}</p>

            <button onClick={onMint}>Mint</button>
            {ownedNfts ? <>
              <div className='nfts'>
                {ownedNfts.map(({ tokenId }) =>
                  <div className='nft-item' key={`own-token-${tokenId}`}>

                    <img src={`https://ipfs.io/ipfs/${BASE_IMAGE_CID}/${tokenId}.png`} />
                    <button onClick={() => onBurn(tokenId)}>Burn</button>
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
