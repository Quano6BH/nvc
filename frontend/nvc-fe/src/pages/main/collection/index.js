import { useContext, useEffect, useState, useMemo } from "react"
import { GlobalContext } from "../../../contexts/GlobalContext"
import './collection.css'
import { getNftDetail, getNftDetailCurrent, getWallet } from "../../../apis/nvcApi";
import loadingGif from '../../../assets/loading.gif'
const Collection = ({ collectionId }) => {
    const { connectedWallet, collection, walletInfo, setWalletInfo, nftContract } = useContext(GlobalContext);
    const [ownedTokenIds, setOwnedTokenIds] = useState();
    const [balance, setBalance] = useState();
    const [selectedToken, setSelectedToken] = useState(null);
    const [nftStats, setNftStats] = useState(null);
    const [nftStatsCurrent, setNftStatsCurrent] = useState(null);
    const [detailLoading, setDetailLoading] = useState(false);
    const ipfs = "https://ikzttp.mypinata.cloud/ipfs/QmYDvPAXtiJg7s8JdRBSLWdgSphQdac8j1YuQNNxcGE1hg"


    useEffect(() => {
        if (!selectedToken)
            return;

        setDetailLoading(true);
        setNftStatsCurrent(null);
        getNftDetail(collectionId, selectedToken, connectedWallet)
            .then((rs) => {
                setNftStats(rs.data)
                getNftDetailCurrent(collectionId, selectedToken, connectedWallet)
                    .then((rs) => {
                        setNftStatsCurrent(rs.data)
                    }).finally(() => {

                        setDetailLoading(false);
                    })
            }).catch(() => {

                setDetailLoading(false);
            })

    }, [selectedToken, collectionId, connectedWallet])

    const onTokenClicked = (tokenId) => {
        setSelectedToken(tokenId)
    }

    useEffect(() => {
        if (!connectedWallet)
            return;

        getWallet(connectedWallet).then((rs) => {
            setWalletInfo(rs.data)
        }).catch((e) => {
            setWalletInfo({ error: "error" })
        })
    }, [connectedWallet])

    useEffect(() => {
        console.log(nftContract)
        if (!nftContract || !connectedWallet)
            return;

        nftContract.methods.balanceOf(connectedWallet)
            .call()
            .then((rs) => {
                setBalance(rs);
            }).catch(e => console.log(e))

        nftContract.methods.tokensOfOwner(connectedWallet)
            .call()
            .then((rs) => {
                setOwnedTokenIds(rs);
            }).catch(e => console.log(e))
        // setOwnedTokenIds([1, 2]);

    }, [nftContract, connectedWallet])

    const getCollectionDuration = ({ startDate, endDate }) => {
        if (!startDate || !endDate)
            return 0;
        const startDateParsed = new Date(Date.parse(startDate))
        const endDateParsed = new Date(Date.parse(endDate))
        return (
            endDateParsed.getMonth() -
            startDateParsed.getMonth() +
            12 * (endDateParsed.getFullYear() - startDateParsed.getFullYear())
        )
    }

    const getDateFormat = (date) => {
        return date.toLocaleDateString("vi-VN");
    }

    const generateNftStatsTable = useMemo(() => {
        if (!collection?.updates) {
            return <></>
        }

        const collectionUpdates = collection?.updates.filter(x => x.type === "Update");

        return collectionUpdates.map(({ from_date, principal, interest, id, buyBack }) => {

            const checkbox = Date.parse(from_date) - Date.now() > 0
            return <tr key={"table-" + id}>
                <td> {getDateFormat(new Date(Date.parse(from_date)))}</ td>
                <td>$ {principal} </td>
                <td>{interest} %</td>
                <td>{checkbox ? "" : "x"}</td>
                <td>{buyBack ? "x" : ""}</td>
            </tr >;
        });
    }, [collection])

    return <>
        {
            walletInfo && !walletInfo.kyc ? <div className="kyc">
                Your wallet need identity verification<br></br>
                Please go to <a href="www.google.com">NVC kyc</a> to verify your identity
            </div>
                : <></>
        }
        {
            !walletInfo?.error
                ?
                <><div className="common-info">
                    <table>
                        <tbody>
                            <tr>
                                <th>Total NFTs hold</th>
                                <td>{balance}</td>
                            </tr>
                            <tr>
                                <th>Interest and principal recorded for {new Date().toLocaleString('default', { month: 'long' })}</th>
                                <td>${walletInfo?.totalEarnInCurrentMonth ?? 0}</td>
                            </tr>
                            <tr>
                                <th>Collection duration</th>
                                <td>{getCollectionDuration(collection)} tháng</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                    <div className="nfts">
                        <div>
                            <h3>Inventory</h3>
                            <div className="inventory">
                                {
                                    ownedTokenIds ? ownedTokenIds.map(tokenId =>
                                        <div key={"own-" + tokenId} className={selectedToken === tokenId ? "token-selected" : ""} onClick={(e) => onTokenClicked(tokenId)}>
                                            <span>{tokenId}</span>
                                            <img width={"100%"} src={`${ipfs}/${tokenId}.png`} alt={`${tokenId}.png`} />


                                        </div>) : <></>
                                }
                            </div>
                        </div>
                        <div>
                            <h3>NFT Stats</h3>
                            <div className={"nft-detail"}>
                                {detailLoading ? <img src={loadingGif} style={{ position: "absolute", margin: "auto" }} alt="loading" /> : <></>}

                                {selectedToken && !detailLoading ? <>
                                    <h4>Token: #{selectedToken}</h4>
                                    <table >
                                        <thead>
                                            <tr>
                                                <th>Date</th>
                                                <th>Pricipal</th>
                                                <th>Interest/Year</th>
                                                <th>Checkbox</th>
                                                <th>Buy back</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {generateNftStatsTable}
                                        </tbody>
                                    </table>

                                    <p>Days holding the NFT in month: {nftStatsCurrent?.holdDaysInCurrentMonth ?? 0}</p></> : ""}

                            </div>
                        </div>

                    </div></>
                :
                <>No info</>
        }


    </>
}

export default Collection;