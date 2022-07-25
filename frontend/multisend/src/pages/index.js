
import { useState, useEffect } from 'react'
import Web3 from 'web3'
import tokenContractInit from '../blockchain/token'
import scatterAbi from './abi/scatter.json'
// import tokenContract from '..blockchain/token'
import styles from '../styles/Home.module.css'
import 'bulma/css/bulma.css'
import getScatterContract from '../blockchain/scatter'
// import dotenv from 'dotenv'

// dotenv().config()
export default function Home() {
  const [web3, setWeb3] = useState()
  const [address, setAddress] = useState()
  const [tokenContractAddress, setTokenContractAddress] = useState()
  const [scatterContract, setScatterContract] = useState();
  const [error, setError] = useState('')
  const [successMsg, setSuccessMsg] = useState('')
  const [tokenBalance, setTokenBalance] = useState()
  const [approvedAmount, setApprovedAmount] = useState()
  const [sendOption, setSendOption] = useState()

  const approveToken = async () => {
    setError('')
    setSuccessMsg('')

    try {
      // setWeb3(window.web3)
      const amount = web3.utils.toWei("222222", 'ether')
      const tokenContract = tokenContractInit(window.web3, tokenContractAddress)
      const tx = await tokenContract.methods.approve(process.env.REACT_APP_SCATTER_CONTRACT_ADDRESS, amount).send({ from: address }).then(async (tx) => {
        await web3.eth.getTransactionReceipt(tx.transactionHash)
        setSuccessMsg('Approved!')
        setApprovedAmount(web3.utils.fromWei(amount, 'ether'))
      })
    } catch (err) {
      console.log(err)
      setError(err.message)
    }
  }

  const sendEther = async () => {
    setError('')
    setSuccessMsg('')
    try {
      const addressAmount = document.getElementById('amount').value
      
      const lines = addressAmount.split("\n")
      const recipientsWithAmount = lines.map((line) => {
        const [recipient, amount] = line.split("=");
        return {
          recipient: String(recipient),
          amount: parseInt(amount)
        }
      })
      const recipients = recipientsWithAmount.map(item => String(item.recipient))
      const amounts = recipientsWithAmount.map(item => item.amount)
      const weiAmounts = recipientsWithAmount.map(item => web3.utils.toWei(String(item.amount), 'ether'))
      const reducer = (accumulator, curr) => accumulator + curr;
      scatterContract.methods.scatterEther(recipients, weiAmounts, true).send({
        from: address,
        gas: 300000,
        value: web3.utils.toWei(String(amounts.reduce(reducer)), 'ether')
      })
    } catch (err) {
      console.log(err)
    }
  }

  const sendToken = async () => {
    setError('')
    setSuccessMsg('')
    try {
      const addressAmount = document.getElementById('amount').value
      const lines = addressAmount.split("\n")
      const recipientsWithAmount = lines.map((line) => {
        const [recipient, amount] = line.split("=");
        return {
          recipient: String(recipient),
          amount: amount
        }
      })
      const tokenContractAddress = document.getElementById('contract').value
      const recipients = recipientsWithAmount.map(item => String(item.recipient))
      const amounts = recipientsWithAmount.map(item => web3.utils.toWei(item.amount, 'ether'))
      scatterContract.methods.scatterToken(tokenContractAddress, recipients, amounts, true).send({
        from: address,
        gas: 300000,
      })
    } catch (err) {
      console.log(err)
    }
  }

  const connectWalletHandler = async () => {
    setError('')
    setSuccessMsg('')
    /* check if MetaMask is installed */
    if (typeof window !== "undefined" && typeof window.ethereum !== "undefined") {
      try {
        const { ethereum } = window
        window.web3 = new Web3(ethereum);
        await ethereum.request({ method: 'eth_requestAccounts' })
        window.web3 = new Web3(window.web3.currentProvider);
        setWeb3(window.web3)
        /* get list of accounts */
        const accounts = await window.web3.eth.getAccounts()
        /* set account 1 to React state */
        await checkNetwork()
        setAddress(accounts[0])
        document.getElementById("btnConnect").innerText = "Switch Wallet"
        /* create local contract copy */
        const sc = getScatterContract(window.web3)
        setScatterContract(sc)
        window.ethereum.on('accountsChanged', async (accounts) => {
          // const accounts = await web3.eth.getAccounts()
          console.log(accounts[0])
          /* set account 1 to React state */
          await checkNetwork()
          setAddress(accounts[0])
          document.getElementById("btnConnect").innerText = "Switch Wallet"
        })
      } catch (err) {
        console.log(err)
        setError(err.message)
      }

    } else {
      /* MetaMask is not installed */
      console.log("Please install MetaMask")
    }
  }

  const isOwner = false

  const checkOwner = async () => {
    const signMessage = window.web3.utils.sha3("hellohello")
    let connectedAccounts = await window.web3.eth.getAccounts()
    window.web3.eth.personal.sign(signMessage, connectedAccounts[0]).then((signature, error) => {
      const util = require('ethereumjs-util');
      // server side
      const { v, r, s } = util.fromRpcSig(signature)
      const address = window.web3.eth.accounts.recover(signMessage, signature)
      console.log(`Address extracted from signature ${address}`)
      if (address == connectedAccounts[0]) {
        isOwner = true
      }
    });
  }

  const checkNetwork = async () => {
    const chainId = 97 // BSC Testnet
    if (window.ethereum.networkVersion !== chainId) {
      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: window.web3.utils.toHex(chainId) }]
        });
      } catch (err) {
        console.log(err)
        // This error code indicates that the chain has not been added to MetaMask
        if (err.code === 4902) {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [
              {
                chainName: 'BSC Testnet',
                chainId: window.web3.utils.toHex(chainId),
                nativeCurrency: { name: 'BNB', decimals: 97, symbol: 'BNB' },
                rpcUrls: ['https://data-seed-prebsc-1-s1.binance.org:8545/']
              }
            ]
          });
        }
      }
    }
  }

  const modifyTokenContractInput = async () => {
    let btnLock = document.getElementById("btnLock")
    let inputTokenContractAddress = document.getElementById("contract")

    var setData = async () => {
      let tokenContract = tokenContractInit(window.web3, inputTokenContractAddress.value)
      setTokenContractAddress(inputTokenContractAddress.value)
      setTokenBalance(window.web3.utils.fromWei(await tokenContract.methods.balanceOf(address).call(), 'ether'))
      setApprovedAmount(window.web3.utils.fromWei(await tokenContract.methods.allowance(address, process.env.REACT_APP_SCATTER_CONTRACT_ADDRESS).call(), 'ether'))
    }

    if (!inputTokenContractAddress.disabled) {
      inputTokenContractAddress.disabled = true
      btnLock.innerHTML = "Unlock"
      await setData()
    } else {
      inputTokenContractAddress.disabled = false
      btnLock.innerHTML = "Lock"
    }
  }

  const changeSendOption = (event) => {
    setSendOption(event.target.value)
  }

  return (
    <div>
      <main className={styles.main}>
        <nav className="navbar mt-4 mb-4">
          <div className="container">
            <div className="navbar-brand">
              <h1>Multisend Toolkit</h1>
            </div>
            <div className="navbar-end">
              {address}
              <button id="btnConnect" onClick={connectWalletHandler} className="button is-link">Connect Wallet</button>
            </div>
          </div>
        </nav>
        <div className="container">
          <section className="mt-5">
            <div className="columns">
              <div className="column is-two-thirds">
                <section className="mt-7">
                  <div className="form-check" onChange={changeSendOption.bind(this)}>
                    <input className="form-check-input" type="radio" name="sendOption" id="ether" value="ether"></input>Send ether<br/>
                    <input className="form-check-input" type="radio" name="sendOption" id="token" value="token"></input>Send token
                  </div>
                </section>
                {sendOption == "token" ?
                <>
                <section className="mt-7" >
                  <p>Token contract</p>
                  <div style={{ display: "flex" }}>
                    <input id="contract" className="form-control" type="text" style={{ width: "60%", height: "50%" }}></input>
                    <button id="btnLock" onClick={modifyTokenContractInput} className="button is-primary is-light" style={{ marginLeft: "0.3em" }}>Lock</button>
                  </div>
                </section>
                <section className="mt-7">
                  <button onClick={approveToken} className="button is-primary is-large is-light mt-3">Approve</button>
                </section>
                <section className="mt-7">
                  <p id="txtBalance">Balance: {tokenBalance}</p>
                  <p id="txtApprovedAmount">Approved amount: {approvedAmount}</p>
                </section>
                <section>
                  <div className="container has-text-danger mt-6">
                    <p>{error}</p>
                  </div>
                </section>
                <section>
                  <div className="container has-text-success mt-6">
                    <p>{successMsg}</p>
                  </div>
                </section>
                </>
                : ""}
                
              </div>
            </div>
          </section>
        </div>
        <div className="container">
          <section className="mt-6">
            <div className="columns">
              <div className="column is-two-thirds">
                <section className="mt-7">
                  <p>Format: address=amount</p>
                  <textarea id="amount" className="form-control" type="text" placeholder='0x609e505827cbaBf618A08C58C3a36589888F18BA=0.5&#10;0x609e505827cbaBf618A08C58C3a36589888F18BA=5&#10;0x609e505827cbaBf618A08C58C3a36589888F18BA=0.3' rows="10" cols="100" style={{ fontSize: "20px", paddingLeft: "0.3em" }}></textarea><br />
                  {sendOption == "token" ?
                  <button onClick={sendToken} className="button is-primary is-large is-light mt-3">Send Token</button>
                  : <button onClick={sendEther} className="button is-primary is-large is-light mt-3">Send Ether</button>}
                </section>
              </div>
            </div>
          </section>
        </div>

      </main>

      <footer className={styles.footer}>
        <p>&copy; 2022 BlackHat</p>
      </footer>
    </div>
  )
}
