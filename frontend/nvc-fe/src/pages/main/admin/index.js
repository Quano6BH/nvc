import { useContext, useEffect, useState } from 'react';
import { getCollectionReport } from '../../../apis/nvcApi';
import { GlobalContext } from '../../../contexts/GlobalContext';
import './admin.css'
const Admin = () => {
    const [report, setReport] = useState();
    const { collection } = useContext(GlobalContext);
    useEffect(() => {
        if (!collection?.id)
            return;
        getCollectionReport(collection?.id).then(rs => {
            setReport(rs.data)
        })

    }, [collection?.id])

    
    return <>
        <div className="admin">
            <table>
                <tbody>
                    <tr>
                        <th>Unique holders</th>
                        <td>{report?.uniqueHolders}</td>
                    </tr>
                    <tr>
                        <th>Interest + principal recorded for all holders</th>
                        <td>{report?.totalPay}</td>
                    </tr>
                    <tr>
                        <th>Interest + principal have not been recorded for all holders</th>
                        <td>{report?.estimate}</td>
                    </tr>
                    <tr>
                        <th>Nft value</th>
                        <td>{collection?.updates[0].principal}</td>
                    </tr>
                    <tr>
                        <th>Total collection value</th>
                        <td>{collection?.updates[0].principal * collection?.totalSupply}</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </>
}

export default Admin;