import { useContext, useEffect, useState, useMemo } from "react"
import { GlobalContext } from "../../../contexts/GlobalContext"
import './collection.css'
import { getNftDetailOfWallet, getWalletCollectionInfo } from "../../../apis/nvcApi";
import loadingGif from '../../../assets/loading.gif'
const Collection = ({ collectionId }) => {
    const { connectedWallet, collection, walletCollectionInfo, setWalletCollectionInfo, nftContract, datetime } = useContext(GlobalContext);
    const [ownedTokenIds, setOwnedTokenIds] = useState();
    const [balance, setBalance] = useState();
    const [selectedToken, setSelectedToken] = useState(null);
    const [nftStats, setNftStats] = useState(null);
    const [detailLoading, setDetailLoading] = useState(false);
    const [ipfs, setIpfs] = useState("");
    // const ipfs = "https://wicked.mypinata.cloud/ipfs/QmTQqEGEXWncTivYaBwarAYcxadqyy6eg4PCmRfXpS8TAQ"

    useEffect(() => {
        setIpfs(`https://wicked.mypinata.cloud/ipfs/${collection?.ipfs}`)
    }, [collection?.ipfs])

    useEffect(() => {
        console.log(selectedToken, selectedToken !== 0 && !selectedToken)
        if (selectedToken !== 0 && !selectedToken)
            return;

        console.log(selectedToken)
        setDetailLoading(true);
        getNftDetailOfWallet(collectionId, selectedToken, connectedWallet, datetime)
            .then((rs) => {
                console.log(rs.data)
                setNftStats(rs.data.data)
            }).catch((e) => {
                console.error(e)
            }).finally(() => {

                setDetailLoading(false);
            })

    }, [selectedToken, collectionId, connectedWallet, datetime])

    const onTokenClicked = (tokenId) => {
        setSelectedToken(tokenId)
    }

    useEffect(() => {
        if (!connectedWallet)
            return;

        getWalletCollectionInfo(connectedWallet, collectionId, datetime).then((rs) => {
            setWalletCollectionInfo(rs.data.data)
        }).catch((e) => {
            setWalletCollectionInfo({ error: "error" })
        })
    }, [connectedWallet, setWalletCollectionInfo, collectionId, datetime])

    useEffect(() => {
        if (!nftContract || !connectedWallet)
            return;

        nftContract.methods.balanceOf(connectedWallet)
            .call()
            .then((rs) => {
                setBalance(rs);
            }).catch(e => console.log(e))

    }, [nftContract, connectedWallet])

    useEffect(() => {
        setOwnedTokenIds(walletCollectionInfo?.nfts)
        // setOwnedTokenIds([1, 2]);

    }, [walletCollectionInfo?.nfts])

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
            walletCollectionInfo && !walletCollectionInfo.kyc ? <div className="kyc">
                Your wallet need identity verification<br></br>
                Please go to <a href="www.google.com">NVC kyc</a> to verify your identity
            </div>
                : <></>
        }
        {
            !walletCollectionInfo?.error
                ?
                <><div className="common-info">
                    <table>
                        <tbody>
                            <tr>
                                <th>Total NFTs currently hold: </th>
                                <td>{balance}</td>
                            </tr>
                            <tr>
                                <th>Interest and principal recorded for {new Date().toLocaleString('default', { month: 'long' })}: </th>
                                <td>${walletCollectionInfo?.totalEarnedInMonth ?? 0}</td>
                            </tr>
                            <tr>
                                <th>Collection duration</th>
                                <td>{getCollectionDuration(collection)} months</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                    <div className="nfts">
                        <div>
                            <h3>Inventory</h3>
                            <div className="inventory">
                                {
                                    ownedTokenIds ? ownedTokenIds.map(({ tokenId, holding }) =>
                                        <div key={"own-" + tokenId} className={selectedToken === tokenId ? "token-selected" : ""} onClick={(e) => onTokenClicked(tokenId)}>
                                            <span>#{tokenId}</span>
                                            <img width={"100%"} src={`${ipfs}`} alt={`${tokenId}.png`} />
                                            {holding}

                                        </div>) : <></>
                                }
                            </div>
                        </div>
                        <div>
                            <h3>NFT Stats</h3>
                            <div className={"nft-detail"}>
                                {detailLoading ? <img src={loadingGif} style={{ position: "absolute", margin: "auto" }} alt="loading" /> : <></>}

                                {(selectedToken || selectedToken === 0) && !detailLoading ? <>
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

                                    <p>Days holding the NFT in month: {nftStats?.current.holdDays ?? 0}</p></> : ""}

                            </div>
                        </div>

                    </div></>
                :
                <>No info</>
        }


    </>
}

export default Collection;