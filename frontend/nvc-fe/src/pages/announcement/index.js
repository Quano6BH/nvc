import { useContext, useEffect, useMemo, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import './announcement.css'
const Announcement = () => {
    const { collection, walletInfo } = useContext(GlobalContext)

    return <>
        { walletInfo && collection?.updates
        ? collection?.updates?.filter(x=>x.type==="Annoucement").map(({ message }) => <section>
            {message}
        </section>) : <></>}

    </>
}

export default Announcement;