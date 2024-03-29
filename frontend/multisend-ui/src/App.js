import logo from './assets/images/logo-bg.png';
import './App.css';

import { loadWeb3, loadContract, connectWallet, shortenAddress, requestApprovalForTokenAsync } from './contracts';
import { useEffect, useState } from 'react';
import scatterAbi from './contracts/abis/scatter.json'
import nftAbi from './contracts/abis/nft.json'
import busdAbi from './contracts/abis/busd.json'
// import { nftContractAddress, scatterContractAddress } from './configs/index.js';
import configs from './configs';
function App() {
  const [scatterContract, setScatterContract] = useState();
  const [nftContract, setNftContract] = useState();
  const [busdContract, setBusdContract] = useState();
  const [allowance, setAllowance] = useState(0);
  const [currentBUSD, setCurrentBUSD] = useState(null);
  const [nftsBurned, setNftsBurned] = useState(null);
  const [nftHolders, setNftHolders] = useState(null);
  const [action, setAction] = useState(null);
  const [approveAmount, setApproveAmount] = useState(0);
  const { nftContractAddress, scatterContractAddress, busdContractAddress } = configs;
  const BASE_IMAGE_CID = "QmSD1Gx6uoF2mGK5jSGdQDbRrWthtM1V219iwYcYyPFzcL";
  const START_BLOCK = 20442946;
  //const busdContractAddress = configs.busdContractAddress;//"0x4e2442A6f7AeCE64Ca33d31756B5390860BF973E";
  // const getFirstBlockNumberOfContract = () => {
  //   nftContract.getPastEvents('Transfer', {
  //     filter: { previousOwner: '0x0000000000000000000000000000000000000000' },
  //     toBlock: 'latest'
  //   })
  //     .then(function (events) {
  //       console.log(events) // same results as the optional callback above
  //       let nfts = events.map((event) => {
  //         const { returnValues } = event;
  //         const { tokenId, to } = returnValues;
  //         return { wallet: to, tokenId: tokenId };
  //       })
  //       // setNftsBurned([...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts]);

  //       setNftsBurned(nfts);
  //     });
  // }
  const [connectedAccount, setConnectedAccount] = useState();

  const changeAccount = (accounts) => {
    if (accounts && accounts.length > 0) {
      setConnectedAccount(accounts[0]);
      loadContract(busdAbi, busdContractAddress, {
        onContractInit: (contract) => { }
      }).then(contract => {
        setBusdContract(contract);
        contract.methods.balanceOf(accounts[0]).call().then(result => {
          setCurrentBUSD(result);
        })
      });
    } else {
      setConnectedAccount(null);
    }
  }
  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        changeAccount(accounts)
      }
    }, [])

  })
  useEffect(() => {
    if (!busdContract || !scatterContract || !connectedAccount)
      return;
    busdContract.methods.allowance(connectedAccount, scatterContract._address)
      .call()
      .then(async (result) => {
        setAllowance(parseInt(result));
      })

  }, [connectedAccount, busdContract, scatterContract])

  useEffect(() => {
    const contractAddress = nftContractAddress;
    loadContract(nftAbi, contractAddress, {
      onContractInit: (contract) => {

        setNftContract(contract)

      }
    });
  }, [nftContractAddress])

  useEffect(() => {
    const contractAddress = scatterContractAddress;
    loadContract(scatterAbi, contractAddress, {
      onContractInit: (contract) => {

        setScatterContract(contract)

      }
    });
  }, [scatterContractAddress])

  const onConnectWallet = async (e) => {
    await connectWallet({
      onAccountConnected: (accounts) => {
        changeAccount(accounts);
      },
      onNetworkChanged: (networkId) => {

      }
    })
  }

  const onGetNftHolders = () => {
    // nftContract.getPastEvents('Transfer', {
    //   // filter: { from: '0x0000000000000000000000000000000000000000' },
    //   fromBlock: START_BLOCK,
    //   toBlock: 'latest'
    // }).then(function (events) {
    //   let nfts = events.map((event) => {
    //     const { returnValues } = event;
    //     const { tokenId, to } = returnValues;
    //     return { wallet: to, tokenId: tokenId };
    //   })

    //   let latest = [];
    //   const groupByTokenId = groupBy(nfts, 'tokenId');
    //   for (let key of Object.keys(groupByTokenId)) {
    //     latest.push({
    //       tokenId: key,
    //       wallet: groupByTokenId[key].at(-1).wallet
    //     })
    //   }
    //   // setNftsBurned([...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts]);
    //   setAction("holder");
    //   setNftHolders(latest);
    // });
    nftContract.getPastEvents('Transfer', {
      // filter: { to: connectedAccount },
      fromBlock: START_BLOCK,
      toBlock: 'latest'
    })
      .then(async (transferEvents) => {
        nftContract.getPastEvents('NftBurned', {
          // filter: { owner: connectedAccount },
          fromBlock: START_BLOCK,
          toBlock: 'latest'
        })
          .then(async (burnedEvents) => {
            let transferNfts = transferEvents.map((event) => {
              const { returnValues } = event;
              const { tokenId, to } = returnValues;
              return { wallet: to, tokenId: tokenId };
            })
            let burnedNfts = burnedEvents.map((event) => {
              const { returnValues } = event;
              const { tokenId, owner } = returnValues;
              return {  wallet: owner, tokenId: tokenId };
            })

            let burnedFlatten = burnedNfts.map(({ tokenId }) => tokenId);
            console.log(burnedFlatten, burnedNfts)
            let nfts = transferNfts.filter(transferNft => !burnedFlatten.includes(transferNft.tokenId));
            // setOwnedNfts([...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts,...nfts]);
            setAction("holder");
            setNftHolders(nfts);
          })

      });
  }

  const onGetBurnedNfts = () => {

    nftContract.getPastEvents('NftBurned', {
      // filter: { owner: connectedAccount },
      fromBlock: START_BLOCK,
      toBlock: 'latest'
    })
      .then(function (events) {
        let nfts = events.map((event) => {
          const { returnValues } = event;
          const { tokenId, owner } = returnValues;
          return { wallet: owner, tokenId: tokenId };
        })
        // setNftsBurned([...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts, ...nfts]);

        setAction("burn");
        setNftsBurned(nfts);
      });
  }

  var groupBy = (array, key) => {
    return array.reduce((rv, x) => {
      (rv[x[key]] = rv[x[key]] || []).push(x);
      return rv;
    }, {});
  };

  const getWalletsWithAmounts = (nfts) => {
    const groupByWallet = groupBy(nfts, 'wallet');
    const walletsWithAmount = []

    for (let key of Object.keys(groupByWallet)) {
      walletsWithAmount.push({
        wallet: key,
        amount: groupByWallet[key].length
      })
    }
    return walletsWithAmount;
  }

  const onMultiSend = async (nfts) => {
    const walletsWithAmount = getWalletsWithAmounts(nfts);

    await scatterContract.methods.scatterBUSD(
      walletsWithAmount.map(({ wallet }) => wallet),
      walletsWithAmount.map(({ amount }) => (amount * 100000000 * 10000000000).toString()),
      true
    ).send({ from: connectedAccount });
  }

  const onRequestApproval = async () => {

    await requestApprovalForTokenAsync(busdContract, scatterContract._address, connectedAccount, (approveAmount * 100000000 * 10000000000).toString());
  }
  const renderApproval = () => allowance <= 0
    ?
    <div>
      <input type={"number"} onChange={e => { setApproveAmount(e.target.value) }} placeholder="input number" defaultValue={1} min={1} />
      <button onClick={onRequestApproval}>Request Approval</button>
    </div>
    : <span style={{ color: "white" }}>Approved: {allowance}</span>;
  const renderAction = (nfts,) => {
    return nfts && nfts.length > 0 ? <>

      {renderApproval()}
      <button onClick={(e) => onMultiSend(nfts)}>Send Monei</button>
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
          {nfts.map(({ wallet, tokenId }) =>
            <tr className='table-row' key={`table-body-${tokenId}`}>
              <td>{shortenAddress(wallet)}</td>
              <td>{tokenId}</td>
              <td><img src={`https://ipfs.io/ipfs/${BASE_IMAGE_CID}/${tokenId}.png`} alt={tokenId} /></td>
            </tr>
          )}
        </tbody>
      </table>
    </> : <></>;
  }
  const renderComponentByAction = (currentAction) => {
    if (!currentAction) return <></>;
    if (currentAction === "burn") {
      return renderAction(nftsBurned);
    } else if (currentAction === "holder") {
      return renderAction(nftHolders);
    }
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
          ? (
            <>
              <p>Nft Contract: {shortenAddress(nftContract?._address)}</p>
              <p>Multisend Contract: {shortenAddress(scatterContract?._address)}</p>
              <p>Connected wallet: {shortenAddress(connectedAccount)}</p>
              <p>BUSD Balance: {currentBUSD}</p>

              {
                action
                  ? renderComponentByAction(action)
                  : <>
                    <button onClick={onGetNftHolders}>Get Nft Holders</button>
                    <button onClick={onGetBurnedNfts}>Get Burned Nfts</button>
                  </>
              }
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
