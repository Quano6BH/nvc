import { useContext } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import Welcome from "./welcome"
import Collection from "./collection"
import './main.css'
import Admin from './admin';
const Main = () => {
    const { connectedWallet } = useContext(GlobalContext)
    const adminWallets = ["0x63412cA517c1EeA44BCaa2B93332f3c39e72277b", "0xCdB996025A437d298c8EfDA33f8538Eb65b48C15"]
    return <main>
        {connectedWallet
            ?

            adminWallets.includes(connectedWallet)
                ? < Admin />
                : < Collection collectionId={1} />
            : <Welcome />}

    </main>
}

export default Main;