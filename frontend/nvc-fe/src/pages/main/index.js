import { useContext, useEffect, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import Welcome from "./welcome"
import Collection from "./collection"
import './main.css'
import Admin from './admin';
import Announcement from '../announcement';
import { signMessage } from '../../contracts';
import { authenticate, requestAuthenticate } from '../../apis/nvcApi';
import loadingGif from "../../assets/loading.gif"
const Main = ({collectionId}) => {
    const { connectedWallet } = useContext(GlobalContext)
    const [loading, setLoading] = useState(true)
    const [isAdmin, setIsAdmin] = useState(0) //0 no one, 1 user, 2 admin
    const [isAuthorized, setIsAuthorized] = useState(false)

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
            if (!user) {
                signMessage(message, connectedWallet).then((signature, error) => {
                    
                    authenticate(connectedWallet, signature).then(resp => {
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
                                ? < Admin collectionId={collectionId} jwt={jwt} />
                                : <p>Please sign the message to connect to admin dashboard</p>

                            : isAdmin === 1
                                ? < Collection collectionId={collectionId} />
                                : <></>
                        : <p>Loading..</p>
                    :  <img src={loadingGif} alt="loading" />}
            </>
            : <Welcome />}

    </main>
}

export default Main;