import { useContext, useEffect, useMemo, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import { connectWallet, shortenAddress } from '../../contracts';
import Countdown from 'react-countdown'
import './header.css'
const Header = () => {
    const { connectedWallet, setConnectedWallet, collection } = useContext(GlobalContext)
    const [endDate, setEndDate] = useState()
    useEffect(() => {
        if (!collection?.endDate)
            return;
        setEndDate(collection?.endDate)
    }, [collection?.endDate])
    const onConnectWallet = async (e) => {
        await connectWallet({
            onAccountConnected: (accounts) => {
                setConnectedWallet(accounts[0]);
            }
        });
    }
    const MemoCountdown = useMemo(() => {
        let end = new Date(Date.parse(collection?.endDate));

        return <Countdown
            date={end}
            intervalDelay={0}
            precision={3}

        // renderer={props => <div>{props.total}</div>}
        ></Countdown>;
    },
        [endDate]);

    return <header>
        <div className='countdown'>
            {MemoCountdown}

        </div>

        <div className='connect-wallet-button' onClick={onConnectWallet}>
            {connectedWallet ? shortenAddress(connectedWallet) : 'Connect Wallet'}
        </div>
        {/* <button onClick={onConnectWallet}>Connect Wallet</button> */}
    </header>
}

export default Header;