import { useContext, useEffect, useState } from 'react';
import { getCollectionReport } from '../../../apis/nvcApi';
import { GlobalContext } from '../../../contexts/GlobalContext';
import './admin.css'
import loadingGif from '../../../assets/loading.gif'
const Admin = (params) => {
    const { jwt, collectionId } = params;
    const [report, setReport] = useState();
    const [error, setError] = useState();
    const [loading, setLoading] = useState(true);
    const { collection } = useContext(GlobalContext);
    useEffect(() => {
        if (!collectionId)
            return;
        setLoading(true)
        getCollectionReport(collectionId, jwt).then(rs => {
            setReport(rs.data)
        }).catch(err => {
            console.log(err)
            setError(err?.response?.data?.message ?? err.message)
        }).finally(() => {
            setLoading(false)
        })

    }, [collectionId, jwt])

    return <>
        {
            !error && !loading ?
                <div className="admin"><table>
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
                : <p style={{ color: "red" }}>{error}</p>
        }
        {
            loading ? <img src={loadingGif} alt="loading" /> : <></>
        }
    </>
}

export default Admin;