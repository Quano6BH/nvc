import logo from './assets/images/logo-bg.png';
import './App.css';

import { loadWeb3, loadContract, connectWallet, shortenAddress } from './contracts';
import { useEffect, useState } from 'react';
import scatterAbi from './contracts/abis/scatter.json'
import nftAbi from './contracts/abis/nft.json'
function App() {
  const [scatterContract, setScatterContract] = useState();
  const [nftContract, setNftContract] = useState();
  const [nftsBurned, setNftsBurned] = useState([]);

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
    const contractAddress = "0xEFDcC78F733ac025F3b9eFBa186c315bAe2Bb3eF";
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
      filter: { from: '0x000000000000000000000000000000' },
      fromBlock: 0,
      toBlock: 'latest'
    }, function (error, events) { console.log(events); })
      .then(function (events) {
        console.log(events) // same results as the optional callback above
      });
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
        {connectedAccount
          ? (<>
            <p>Connected wallet: {shortenAddress(connectedAccount)}</p>
            {nftsBurned ? <>
              <table>
                <thead>
                  <tr>
                    <th>Wallet address</th>
                    <th>Token ID</th>
                  </tr>
                </thead>
                <tbody>
                  {nftsBurned.map(({ wallet, tokenId }) => {
                    <tr>
                      <td>{wallet}</td>
                      <td>{tokenId}</td>
                    </tr>
                  })}
                </tbody>
              </table>
            </> : <></>}
            <button onClick={onFetchWallets}>Fetch wallets</button>
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
