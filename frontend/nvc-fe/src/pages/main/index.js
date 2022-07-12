import { useContext, useEffect, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import Welcome from "./welcome"
import Collection from "./collection"
import './main.css'
import Admin from './admin';
import Announcement from '../announcement';
import { signMessage } from '../../contracts';
import { authenticate, requestAuthenticate } from '../../apis/nvcApi';
const Main = () => {
    const { connectedWallet } = useContext(GlobalContext)
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(false)
    const [isAuthorized, setIsAuthorized] = useState(false)
    const adminWallets = ["0x63412cA517c1EeA44BCaa2B93332f3c39e72277b", "0xCdB996025A437d298c8EfDA33f8538Eb65b48C15", "0x79537C2ad640E6d93E7c06C85aBa28AbC40B8301"]

    const [jwt, setJwt] = useState("")
    useEffect(() => {
        if (!connectedWallet)
            return;

        // setLoading(true)
        requestAuthenticate(connectedWallet).then((rs) => {
            const { message, user } = rs.data;
            console.log(rs.data)
            if (!user) {
                setIsAdmin(true)
                signMessage(message, connectedWallet).then((signature, error) => {
                    authenticate(connectedWallet, signature).then(resp => {
                        const jwtData = resp.data;
                        setIsAuthorized(true)
                        setJwt(jwtData)
                    })

                })

            }
        }).finally(() => {

            setLoading(false)
        })


    }, [connectedWallet])

    return <main>
        {connectedWallet
            ?
            <>
                <Announcement />
                {!loading
                    ? isAdmin
                        ?
                        isAuthorized
                            ? < Admin jwt={jwt} />
                            : <p>Please sign the message to connect to admin dashboard</p>

                        : < Collection collectionId={1} />
                    : <p>Loading..</p>}
            </>
            : <Welcome />}

    </main>
}

export default Main;