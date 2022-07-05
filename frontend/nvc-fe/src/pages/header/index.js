import { useContext, useEffect, useMemo, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import { connectWallet } from '../../contracts';
import Countdown from 'react-countdown'
import './header.css'
const Header = () => {
    const { connectedWallet, setConnectedWallet, collection } = useContext(GlobalContext)
    const onConnectWallet = async (e) => {
        await connectWallet({
            onAccountConnected: (accounts) => {
                setConnectedWallet(accounts[0]);
            }
        });
    }
    const MemoCountdown = useMemo(() => {
        let end = new Date(Date.parse(collection?.end_date));
        setInterval(() => { end = new Date(end - 1000) }, 1000)

        return <>{`Days: s${end.getDay()}/ Hours: ${end.getHours()}/ Minutes: ${end.getMinutes()}/ Seconds: ${end.getSeconds()}`}</>;
    },
        [collection?.end_date]);

    console.log(collection)
    console.log(collection?.end_date)
    return <header>
        <div className='countdown'>
            {MemoCountdown}

        </div>
        {connectedWallet}
        <div className='connect-wallet-button' onClick={onConnectWallet}>
            Connect Wallet
        </div>
        {/* <button onClick={onConnectWallet}>Connect Wallet</button> */}
    </header>
}

export default Header;