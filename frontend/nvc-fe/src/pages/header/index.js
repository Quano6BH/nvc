import { useContext, useMemo } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import { connectWallet, shortenAddress, switchNetwork } from '../../contracts';
import Countdown from 'react-countdown'
import './header.css'
const Header = () => {
    const { connectedWallet, setConnectedWallet, collection } = useContext(GlobalContext)

    const onConnectWallet = async (e) => {
        await switchNetwork(
            {
                chainId: 97,
                chainName: "Binance Smart Chain Testnet",
                nativeCurrency: {
                    name: 'Binance Coin',
                    symbol: 'tBNB',
                    decimals: 18
                },
                rpcUrls: ['https://data-seed-prebsc-1-s1.binance.org:8545'],
                blockExplorerUrls: ['https://testnet.bscscan.com']
            });

        await connectWallet({
            onAccountConnected: (accounts) => {
                if (connectedWallet !== accounts[0]) {
                    setConnectedWallet(accounts[0]);
                }
            }
        });
    }

    // parse each string as a Date object and sort them in ascending order
    function sortDates(dates) {
        return dates.map(function (date) {
            return new Date(date).getTime();
        }).sort(function (a, b) {
            return a - b;
        });
    }


    // remove any dates in the past, and get the first child of the array of remaining dates


    const MemoCountdown = useMemo(() => {
        if (!collection?.updates)
            return <>loading</>
        let dates = collection?.updates.map(x => new Date(Date.parse(x.from_date)));

        var orderedDates = sortDates(dates);
        // console.log(orderedDates)
        var nextDate = orderedDates.filter(function (date) {
            // console.log(Date.now(), date, Date.now() - date)
            return (Date.now() - date) < 0;
        })[0];

        // console.log(Date.now(), new Date(nextDate))

        return <>

            <Countdown
                date={nextDate}
                intervalDelay={0}
                precision={3}


                renderer={({ days, hours }) => <div>Next payment countdown: {days} days {hours} hours</div>}
            ></Countdown>
        </>;
    },
        [collection?.updates]);

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