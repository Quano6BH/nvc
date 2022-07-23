import { useContext, useEffect, useState, useRef } from 'react';
import { getCollectionReport, updateKyc } from '../../../apis/nvcApi';
import { GlobalContext } from '../../../contexts/GlobalContext';
import './admin.css'
import loadingGif from '../../../assets/loading.gif'
import Web3 from 'web3'
const Admin = (params) => {
    const { jwt, collectionId } = params;
    const [report, setReport] = useState();
    const [error, setError] = useState();
    const [loading, setLoading] = useState(true);
    const [errMessage, setErrMessage] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const { collection } = useContext(GlobalContext);
    const ref = useRef(null);

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

    const validateAddresses = (addresses) => {
        for (let address of addresses) {
            if (!Web3.utils.checkAddressChecksum(address))
                return false;

        }

        return true;
    }

    const onKycSubmit = (e) => {
        const addresses = ref.current.value.split("\n")
        setErrMessage(null)
        setSuccessMessage(null)
        if (!ref.current.value) {
            setErrMessage("empty addresses")
            return;
        }
        if (!validateAddresses(addresses)) {
            setErrMessage("please check addresses checksum")
            return;
        }
        const data = {
            kyc: true,
            addresses
        }

        updateKyc(data, jwt).then(rs => {
            setSuccessMessage("Success")
        }).catch(e => {
            setErrMessage(e.message)

        })
    }

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
                            <td>${report?.totalPay}</td>
                        </tr>
                        <tr>
                            <th>Interest + principal have not been recorded for all holders</th>
                            <td>${report?.estimate}</td>
                        </tr>
                        <tr>
                            <th>Nft value</th>
                            <td>${collection?.updates[0].principal}</td>
                        </tr>
                        <tr>
                            <th>Total collection value</th>
                            <td>${collection?.updates[0].principal * collection?.totalSupply}</td>
                        </tr>
                    </tbody>
                </table>
                </div>
                : <p style={{ color: "red" }}>{error}</p>
        }
        {
            loading ? <img src={loadingGif} alt="loading" /> : <></>
        }
        <br />
        <fieldset>
            <legend>Kyc:</legend>
            {successMessage ? <p style={{ color: "green" }}>{successMessage}</p> : <></>}

            {errMessage ? <p style={{ color: "red" }}>{errMessage}</p> : <></>}
            <textarea ref={ref} id="message" name="message" className='boxsizingBorder'>

            </textarea>
            <button className='submit-button' onClick={onKycSubmit}>Submit</button>
        </fieldset>

    </>
}

export default Admin;