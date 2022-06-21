import logo from './assets/images/logo-bg.png';
import './App.css';

import { loadWeb3, loadContract, connectWallet, shortenAddress } from './contracts';
import { useEffect, useState } from 'react';
import scatterAbi from './contracts/abis/scatter.json'
import nftAbi from './contracts/abis/nft.json'
function App() {
  const [scatterContract, setScatterContract] = useState();
  const [nftContract, setNftContract] = useState();
  const [nftsBurned, setNftsBurned] = useState(null);

  const BASE_IMAGE_CID = "QmSD1Gx6uoF2mGK5jSGdQDbRrWthtM1V219iwYcYyPFzcL";

  const [connectedAccount, setConnectedAccount] = useState();
  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        if (accounts && accounts.length > 0) {
          setConnectedAccount(accounts[0])
        } else {
          setConnectedAccount(null)

        }
      }
    })

  }, [connectedAccount])
  useEffect(() => {
    const contractAddress = "0xA7e36cbe8C97D9FB48dBF5587fD7E78cF13e552E";
    loadContract(nftAbi, contractAddress, {
      onContractInit: (contract) => {

        setNftContract(contract)

      }
    });
  }, [nftAbi])
  useEffect(() => {
    const contractAddress = "0xEFDcC78F733ac025F3b9eFBa186c315bAe2Bb3eF";
    loadContract(scatterAbi, contractAddress, {
      onContractInit: (contract) => {

        setScatterContract(contract)

      }
    });
  }, [scatterAbi])
  const onConnectWallet = async (e) => {
    await connectWallet({
      onAccountConnected: (accounts) => {
        if (accounts && accounts.length > 0) {
          setConnectedAccount(accounts[0]);
        } else {
          setConnectedAccount(null);
        }
      },
      onNetworkChanged: (networkId) => {

      }
    })
  }
  const onFetchWallets = () => {
    nftContract.getPastEvents('Transfer', {
      filter: { from: '0x0000000000000000000000000000000000000000' },
      fromBlock: 0,
      toBlock: 'latest'
    })
      .then(function (events) {
        console.log(events) // same results as the optional callback above
        let nfts = events.map((event) => {
          const { returnValues } = event;
          const { tokenId, to } = returnValues;
          return { wallet: to, tokenId: tokenId };
        })
        // setNftsBurned([...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts]);

        setNftsBurned(nfts);
      });
  }
  var groupBy = (array, key) => {
    return array.reduce((rv, x) => {
      (rv[x[key]] = rv[x[key]] || []).push(x);
      return rv;
    }, {});
  };
  const onMultiSend = (e) => {
    const groupByWallet = groupBy(nftsBurned, 'wallet');
    const walletsWithAmount = []
    
    for( let key of Object.keys(groupByWallet)){
      walletsWithAmount.push({
        wallet : key,
        amount : groupByWallet[key].length
      })
    }
    console.log(walletsWithAmount)
  }

  const shortenAddress = (address) => address.substring(0, 5) + "....." + address.substring(address.length - 4, address.length)
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
            <p>Nft Contract: {shortenAddress(nftContract?._address)}</p>
            <p>Multisend Contract: {shortenAddress(nftContract?._address)}</p>
            <p>Connected wallet: {shortenAddress(connectedAccount)}</p>
            {nftsBurned && nftsBurned.length > 0 ? <>

              <button onClick={onMultiSend}>Send Monei</button>
              <br />
              <table>
                <thead>
                  <tr>
                    <th>Wallet address</th>
                    <th>Token ID</th>
                    <th>Image</th>
                  </tr>
                </thead>
                <tbody>
                  {nftsBurned.map(({ wallet, tokenId }) =>
                    <tr className='table-row' key ={`table-body-${tokenId}`}>
                      <td>{shortenAddress(wallet)}</td>
                      <td>{tokenId}</td>
                      <td><img src={`https://ipfs.io/ipfs/${BASE_IMAGE_CID}/${tokenId}.png`} /></td>
                    </tr>
                  )}
                </tbody>
              </table>
            </> : <>
              <button onClick={onFetchWallets}>Fetch wallets</button>
            </>}
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
