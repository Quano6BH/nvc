import { useContext, useEffect, useState } from 'react';
import { getCollectionReport } from '../../../apis/nvcApi';
import { GlobalContext } from '../../../contexts/GlobalContext';
import './admin.css'
const Admin = () => {
    const [report, setReport] = useState();
    const { collection } = useContext(GlobalContext);
    useEffect(() => {
        getCollectionReport(collection?.id).then(rs => {
            setReport(rs.data)
        })

    }, [collection?.id])
    return <>
        <div class="admin">
            <p>Unique holders: {report?.uniqueHolders}</p>
            <p>Lãi + gốc phải trả cho toàn bộ holder:{report?.totalPay}</p>
            <p>Estimate trong 30 ngày:{report?.estimate}</p>

        </div>
    </>
}

export default Admin;