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
        <div class="admin">
            <table>
                <tbody>
                    <tr>
                        <th>Unique holders</th>
                        <td>{report?.uniqueHolders}</td>
                    </tr>
                    <tr>
                        <th>Lãi + gốc đã ghi nhận cho toàn bộ holder</th>
                        <td>{report?.totalPay}</td>
                    </tr>
                    <tr>
                        <th>Lãi + gốc chưa ghi nhận cho toàn bộ holder</th>
                        <td>{report?.estimate}</td>
                    </tr>
                    <tr>
                        <th>Giá trị từng NFT</th>
                        <td>{collection?.updates[0].principal}</td>
                    </tr>
                    <tr>
                        <th>Tổng giá trị bộ sưu tập</th>
                        <td>{collection?.updates[0].principal * collection?.totalSupply}</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </>
}

export default Admin;