import Web3 from 'web3';

const requestApprovalForTokenAsync = async (contract, forAccount, amount) => {
    await contract.methods.approve(forAccount, amount).send({ from: forAccount });
}

const isMetaMaskInstalled = () => {
    const { ethereum } = window;
    return Boolean(ethereum && ethereum.isMetaMask);
};

const loadContract = async (contractAbi, contractAddress, { onContractInit }) => { 
    window.web3 = new Web3(window.web3.currentProvider);
    const web3 = window.web3;
    const contract = new web3.eth.Contract(contractAbi, contractAddress);

    onContractInit(contract);

    return contract;
}

const loadWeb3 = async ({ onAccountChanged }) => {
    try {
        if (!isMetaMaskInstalled) return alert('Please install Metamask');
        const { ethereum } = window;
        ethereum.on('accountsChanged', (accounts) => {
            onAccountChanged(accounts);
            // if (!accounts) {
            //     setGlobalState('connectedAccount', null);

            // } else {
            //     setGlobalState('connectedAccount', accounts[0])

            // }

        });

    } catch (e) {
        console.error(e)
    }
}


const connectWallet = async ({ onAccountConnected, onNetworkChanged }) => {
    try {
        const { ethereum } = window
        window.web3 = new Web3(ethereum);
        await ethereum.enable();

        window.web3 = new Web3(window.web3.currentProvider);
        const web3 = window.web3;

        const accounts = await web3.eth.getAccounts()

        const networkId = await web3.eth.net.getId()

        onAccountConnected(accounts, networkId)
        // setGlobalState('connectedAccount', accounts[0])

        // NotificationManager.info(`Wallet ${accounts[0]} connected.`);

        // if (networkId !== 1)
        //     NotificationManager.warning(`Please be aware you are not connecting to mainnet.`);


    } catch (e) {
        console.error(e)
        alert('Please connect your metamask wallet!')
    }
}


const shortenAddress = (address) => address.substring(0, 5) + "....." + address.substring(address.length - 4, address.length)
export { connectWallet, loadWeb3, loadContract, shortenAddress, requestApprovalForTokenAsync }