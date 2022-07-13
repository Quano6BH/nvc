import { useContext, useEffect, useState, useMemo } from "react"
import { GlobalContext } from "../../../contexts/GlobalContext"
import { loadContract } from "../../../contracts";
import nftAbi from '../../../contracts/abis/nft.json'
import configs from '../../../configs'
import './collection.css'
import { getNftDetail, getNftDetailCurrent } from "../../../apis/nvcApi";
const Collection = ({ collectionId }) => {
    const { connectedWallet, collection, walletInfo } = useContext(GlobalContext);
    const [nftContract, setNftContract] = useState();
    const [ownedTokenIds, setOwnedTokenIds] = useState();
    const [balance, setBalance] = useState();
    const [selectedToken, setSelectedToken] = useState(null);
    const [nftStats, setNftStats] = useState(null);
    const [nftStatsCurrent, setNftStatsCurrent] = useState(null);
    const [detailLoading, setDetailLoading] = useState(false);
    const { nftContractAddress } = configs;
    const ipfs = "https://ikzttp.mypinata.cloud/ipfs/QmYDvPAXtiJg7s8JdRBSLWdgSphQdac8j1YuQNNxcGE1hg"

    useEffect(() => {
        loadContract(nftAbi, nftContractAddress,
            {
                onContractInit: async (contract) => {
                    setNftContract(contract);
                }
            })
    }, [nftContractAddress])

    useEffect(() => {
        if (!selectedToken)
            return;

        setDetailLoading(true);
        getNftDetail(collection?.id, selectedToken, connectedWallet)
            .then((rs) => {
                setNftStats(rs.data)
                getNftDetailCurrent(collection?.id, selectedToken, connectedWallet)
                    .then((rs) => {
                        setNftStatsCurrent(rs.data)
                    }).finally(() => {

                        setDetailLoading(false);
                    })
            }).catch(() => {

                setDetailLoading(false);
            })

    }, [selectedToken, collection?.id, connectedWallet])

    // useEffect(() => {
    //     if (!selectedToken)
    //         return;

    //     setNftStats({
    //         currentOwner: "0x..",
    //         holdDaysInCurrentMonth: 3,//number of days the NFT owned by the owner
    //         collectionId: 1,
    //         earnings: [
    //             {
    //                 month: 1,//1-12, 
    //                 principalEarned: 12,//by $,gốc nhận được của tháng 1 
    //                 interestEarned: 0.1,//by $, lãi nhận được của tháng 1
    //                 interestRate: 0.1,//by %, % lãi của tháng
    //                 principalRate: 20//by $, tiền gốc mỗi NFT của tháng
    //             },
    //             {
    //                 month: 2,//1-12, 
    //                 principalEarned: 12,//by $,gốc nhận được của tháng 1 
    //                 interestEarned: 0.1,//by $, lãi nhận được của tháng 1
    //                 interestRate: 0.1,//by %, % lãi của tháng
    //                 principalRate: 20//by $, tiền gốc mỗi NFT của tháng
    //             }
    //         ]
    //     })



    // }, [selectedToken])

    const onTokenClicked = (tokenId) => {
        setSelectedToken(tokenId)
    }


    useEffect(() => {
        if (!nftContract || !connectedWallet)
            return;
        console.log(nftContract)

        nftContract.methods.balanceOf(connectedWallet)
            .call()
            .then((rs) => {
                setBalance(rs);
            }).catch(e => console.log(e))
        // setBalance(2);
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

    const getMonthsDiff = (d1, d2) => {
        let monthsDiff = (d2.getFullYear() - d1.getFullYear()) * 12;
        monthsDiff -= d1.getMonth();
        monthsDiff += d2.getMonth();
        return monthsDiff <= 0 ? 0 : monthsDiff;
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
            // console.log(nftStats?.earnings, id)
            const nftStat = nftStats?.earnings ? nftStats?.earnings.filter(x => x.updateAppliedId === id)[0] : null;
            // console.log(from_date)
            const checkbox = Date.parse(from_date) - Date.now() > 0
            return <tr>
                <td> {getDateFormat(new Date(Date.parse(from_date)))}</ td>
                <td>$ {principal} </td>
                <td>{interest} %</td>
                <td>{checkbox ? "" : "x"}</td>
                <td>{buyBack ? "x" : ""}</td>
            </tr >;
        });
    }, [collection, nftStats])
    return <>
        {
            walletInfo && !walletInfo.kyc ? <div className="kyc">
                Ví của bạn chưa được xác minh danh tính<br></br>
                Vui lòng vào link <a href="www.google.com">NVC kyc</a> để xác minh danh tính
            </div>
                : <></>
        }
        {
            walletInfo
                ?
                <><div className="common-info">
                    <table>
                        <tr>
                            <th>Tổng NFTs đang giữ</th>
                            <td>{balance}</td>
                        </tr>
                        <tr>
                            <th>Lãi và gốc ghi nhận cho tháng {new Date().getMonth() + 1}</th>
                            <td>${walletInfo?.totalEarnInCurrentMonth ?? 0}</td>
                        </tr>
                        <tr>
                            <th>Thời hạn của hợp đồng</th>
                            <td>{getCollectionDuration(collection)} tháng</td>
                        </tr>
                    </table>
                    {/* <h4>Tổng NFTs đang giữ: {balance}</h4>
            <h4>Lãi và gốc ghi nhận cho tháng {new Date().getMonth() + 1}:  </h4>
            <h4>Thời hạn của hợp đồng: {getCollectionDuration(collection)} tháng</h4> */}
                </div>
                    <div className="nfts">
                        <div>
                            <h3>Kho đồ</h3>
                            <div className="inventory">
                                {
                                    ownedTokenIds ? ownedTokenIds.map(tokenId =>
                                        <div className={selectedToken === tokenId ? "token-selected" : ""} onClick={(e) => onTokenClicked(tokenId)}>
                                            <span>{tokenId}</span>
                                            <img width={"100%"} src={`${ipfs}/${tokenId}.png`} alt={`${tokenId}.png`} />


                                        </div>) : <></>
                                }
                            </div>
                        </div>
                        <div>
                            <h3>Chi tiết</h3>
                            <div className={detailLoading ? "table-loading nft-detail" : "nft-detail"}>
                                {selectedToken ? <>
                                    <h4>Token: #{selectedToken}</h4>
                                    <table >
                                        <thead>
                                            <tr>
                                                <th>Ngày</th>
                                                <th>Gốc</th>
                                                <th>Lãi/năm</th>
                                                <th>Chốt</th>
                                                <th>Buy back</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {generateNftStatsTable}
                                        </tbody>
                                    </table>

                                    <p>Số ngày hold nft của ví trong tháng: {nftStatsCurrent?.holdDaysInCurrentMonth ?? 0}</p></> : ""}

                            </div>
                        </div>

                    </div></>
                :
                <>No info</>
        }


    </>
}

export default Collection;