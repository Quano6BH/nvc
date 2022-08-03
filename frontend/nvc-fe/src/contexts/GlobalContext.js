import { createContext, useEffect, useState } from "react";
import { loadContract } from "../contracts";
import configs from '../configs'
import nftAbi from '../contracts/abis/nft.json'
import { toChecksumAddress, checkAddressChecksum } from 'web3-utils'
const { nftContractAddress } = configs;

export const GlobalContext = createContext({});

export const GlobalContextProvider = ({ children }) => {

    const [connectedWallet, setConnectedWallet] = useState();
    const [walletCollectionInfo, setWalletCollectionInfo] = useState(null);
    const [collection, setCollection] = useState({});
    const [nftContract, setNftContract] = useState(null);
    const [datetime, setDatetime] = useState(new Date());

    // You can choose to wrap this in a useMemo if you want to be extra careful about potential rerenders
    const globalContextStore = {
        connectedWallet,
        walletCollectionInfo,
        setConnectedWallet,
        collection,
        setCollection,
        setWalletCollectionInfo,
        nftContract,
        datetime,
        setDatetime
    }

    useEffect(() => {
        // console.log(!checkAddressChecksum(collection?.address))
        if (!collection?.address)
            return;

        // console.log(collection?.address, toChecksumAddress(collection?.address))
        loadContract(nftAbi, toChecksumAddress(collection?.address.trim()),
            {
                onContractInit: async (contract) => {
                    setNftContract(contract);
                }
            })
    }, [collection?.address])

    return <GlobalContext.Provider value={globalContextStore}>{children}</GlobalContext.Provider>
};