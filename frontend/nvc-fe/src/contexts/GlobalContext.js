import { createContext, useEffect, useState } from "react";
import { getWallet } from "../apis/nvcApi";
export const GlobalContext = createContext({});

export const GlobalContextProvider = ({ children }) => {

    const [connectedWallet, setConnectedWallet] = useState();
    const [walletInfo, setWalletInfo] = useState(null);
    const [collection, setCollection] = useState({});

    // You can choose to wrap this in a useMemo if you want to be extra careful about potential rerenders
    const globalContextStore = {
        connectedWallet,
        walletInfo,
        setConnectedWallet,
        collection,
        setCollection
    }
    useEffect(() => {
        if (!connectedWallet)
            return;
            
        getWallet(connectedWallet).then((rs) => {
            setWalletInfo(rs.data)
        })
    }, [connectedWallet])

    return <GlobalContext.Provider value={globalContextStore}>{children}</GlobalContext.Provider>
};