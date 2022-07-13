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
    const [isAdmin, setIsAdmin] = useState(0) //0 no one, 1 user, 2 admin
    const [isAuthorized, setIsAuthorized] = useState(false)
    const adminWallets = ["0x63412cA517c1EeA44BCaa2B93332f3c39e72277b", "0xCdB996025A437d298c8EfDA33f8538Eb65b48C15", "0x79537C2ad640E6d93E7c06C85aBa28AbC40B8301"]

    const [jwt, setJwt] = useState("")
    useEffect(() => {
        if (!connectedWallet)
            return;

        // setLoading(true)

        // console.log("--------------" + connectedWallet)
        setIsAuthorized(false)
        setIsAdmin(0)
        setJwt("")
        setLoading(true)
        requestAuthenticate(connectedWallet).then((rs) => {
            const { message, user } = rs.data;
            // console.log("--------------" + connectedWallet, rs, user)
            if (!user) {
                console.log("sign--------------" + connectedWallet, rs, user)
                signMessage(message, connectedWallet).then((signature, error) => {
                    
                    // console.log("signMessage.then--------------" + connectedWallet, rs, user)
                    authenticate(connectedWallet, signature).then(resp => {
                        // console.log("authenticate--------------" + connectedWallet, rs, user)
                        const jwtData = resp.data;
                        setIsAuthorized(true)
                        setJwt(jwtData)
                    })

                }).finally(() => {

                    setLoading(false)
                })

                setIsAdmin(2)
            } else {

                setIsAdmin(1)
            }

            setLoading(false)
        }).catch(() => {

            setLoading(false)
        })


    }, [connectedWallet])

    return <main>
        {connectedWallet
            ?
            <>
                <Announcement />
                {!loading
                    ? isAdmin !== 0
                        ? isAdmin === 2
                            ? isAuthorized
                                ? < Admin jwt={jwt} />
                                : <p>Please sign the message to connect to admin dashboard</p>

                            : isAdmin === 1
                                ? < Collection collectionId={3} />
                                : <></>
                        : <p>Loading..</p>
                    : <>Loading..</>}
            </>
            : <Welcome />}

    </main>
}

export default Main;