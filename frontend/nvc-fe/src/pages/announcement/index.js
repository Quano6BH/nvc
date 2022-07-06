import { useContext, useEffect, useMemo, useState } from 'react';
import { GlobalContext } from '../../contexts/GlobalContext';
import './announcement.css'
const Announcement = () => {
    const { collection } = useContext(GlobalContext)

    return <>
        {collection?.updates 
        ? collection?.updates.map(({ message }) => <section>
            Announcement: We will buy back 10%
        </section>) : <></>}

    </>
}

export default Announcement;