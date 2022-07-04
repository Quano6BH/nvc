import { useContext } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import { connectWallet } from '../../contracts';
import './header.css'
const Header = () => {
    const { connectedWallet, setConnectedWallet } = useContext(GlobalContext)
    const onConnectWallet = async (e) => {
        await connectWallet({
            onAccountConnected: (accounts) => {
                setConnectedWallet(accounts[0]);
            }
        });
    }


    return <header>
        <div className='countdown'>Countdown</div>
        {connectedWallet}
        <div className='connect-wallet-button' onClick={onConnectWallet}>
        Connect Wallet
        </div>
        {/* <button onClick={onConnectWallet}>Connect Wallet</button> */}
    </header>
}

export default Header;