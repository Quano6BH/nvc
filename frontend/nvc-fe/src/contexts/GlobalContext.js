import { createContext, useState } from "react";

export const GlobalContext = createContext({});

export const GlobalContextProvider = ({ children }) => {

    const [connectedWallet, setConnectedWallet] = useState();

    // You can choose to wrap this in a useMemo if you want to be extra careful about potential rerenders
    const globalContextStore = {
        connectedWallet,
        setConnectedWallet,

    }
    return <GlobalContext.Provider value={globalContextStore}>{children}</GlobalContext.Provider>
};