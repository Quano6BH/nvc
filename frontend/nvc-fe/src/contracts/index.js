import Web3 from 'web3';

const requestApprovalForTokenAsync = async (contract, spender, owner, amount) => {
    await contract.methods.approve(spender, amount).send({ from: owner });
}

const isMetaMaskInstalled = () => {
    const { ethereum } = window;
    return Boolean(ethereum && ethereum.isMetaMask);
};

const loadContract = async (contractAbi, contractAddress, { onContractInit }) => {
    window.web3 = new Web3(window.web3.currentProvider);
    const web3 = window.web3;
    const contract = new web3.eth.Contract(contractAbi, contractAddress);
    // console.log(await web3.eth.net.getId())
    await onContractInit(contract);

    return contract;
}

const loadWeb3 = async ({ onAccountChanged }) => {
    try {
        if (!isMetaMaskInstalled) return alert('Please install Metamask');
        const { ethereum } = window;
        const accountChanged = (accounts) => {
            onAccountChanged(accounts);
        };
        ethereum.removeListener("accountsChanged", accountChanged);
        ethereum.on('accountsChanged', accountChanged);

    } catch (e) {
        console.error(e)
    }
}


const connectWallet = async ({ onAccountConnected }) => {
    try {
        const { ethereum } = window
        window.web3 = new Web3(ethereum);
        await ethereum.enable();

        window.web3 = new Web3(window.web3.currentProvider);
        const web3 = window.web3;

        const accounts = await web3.eth.getAccounts()
        // const accounts = ethereum.request({ method: 'eth_accounts' })
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

const signMessage = async (message, account) => {
    return window.web3.eth.personal.sign(message, account);
};
const switchNetwork = async ({ chainId, chainName = 'Binance Smart Chain', ...others }) => {
    // {
    //     chainId: Web3.utils.toHex(chainId),
    //     chainName: ,
    //     nativeCurrency: {
    //         name: 'Binance Coin',
    //         symbol: 'BNB',
    //         decimals: 18
    //     },
    //     rpcUrls: ['https://bsc-dataseed.binance.org/'],
    //     blockExplorerUrls: ['https://bscscan.com']
    // }
    const { ethereum } = window
    window.web3 = new Web3(ethereum);
    await ethereum.enable();

    window.web3 = new Web3(window.web3.currentProvider);
    const web3 = window.web3;

    const currentChainId = await web3.eth.net.getId()

    if (currentChainId !== chainId) {
        try {
            await web3.currentProvider.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: Web3.utils.toHex(chainId) }],
            });
        } catch (switchError) {
            if (switchError.code === 4902) {
                try {
                    await web3.currentProvider.request({
                        method: 'wallet_addEthereumChain',
                        params: [{
                            chainId: Web3.utils.toHex(chainId),
                            chainName: chainName,
                            ...others
                        }]
                    });
                } catch (addError) {
                    console.error(addError);
                }
            }
        }
    }
}

const shortenAddress = (address) => address.substring(0, 5) + "....." + address.substring(address.length - 4, address.length);

export { connectWallet, loadWeb3, loadContract, shortenAddress, requestApprovalForTokenAsync, signMessage, switchNetwork }