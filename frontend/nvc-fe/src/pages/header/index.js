import { useContext, useEffect, useMemo, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import { connectWallet, shortenAddress } from '../../contracts';
import Countdown from 'react-countdown'
import './header.css'
const Header = () => {
    const { connectedWallet, setConnectedWallet, collection } = useContext(GlobalContext)
    const [endDate, setEndDate] = useState()
    useEffect(() => {
        // console.log(collection)
        if (!collection?.endDate)
            return;
        setEndDate(collection?.endDate)
    }, [collection?.endDate])
    const onConnectWallet = async (e) => {
        await connectWallet({
            onAccountConnected: (accounts) => {
                console.log("connectWallet", accounts[0], connectedWallet)
                if (connectedWallet != accounts[0]) {
                    console.log("change", accounts[0], connectedWallet)
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