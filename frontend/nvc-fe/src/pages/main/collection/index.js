import { useContext, useEffect, useState } from "react"
import { GlobalContext } from "../../../contexts/GlobalContext"
import { loadContract } from "../../../contracts";
import nftAbi from '../../../contracts/abis/nft.json'
import configs from '../../../configs'
import './collection.css'
const Collection = ({ collectionId }) => {
    const { connectedWallet } = useContext(GlobalContext);
    const [nftContract, setNftContract] = useState();
    const [ownedTokenIds, setOwnedTokenIds] = useState();
    const [balance, setBalance] = useState();
    const { nftContractAddress } = configs;
    useEffect(() => {
        loadContract(nftAbi, nftContractAddress,
            {
                onContractInit: async (contract) => {
                    setNftContract(contract);
                }
            })
    }, [nftAbi, nftContractAddress])
    useEffect(() => {
        if (!nftContract || !connectedWallet)
            return;
        console.log(nftContract, connectedWallet)
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

    }, [nftContract, connectedWallet])
    return <>
        <div className="common-info">

            <h1>Tong NFT dang hold: {balance}</h1>
            <h1>Lai va goc ghi nhan cho thang</h1>
            <h1>Thoi han cua bo NFT</h1>
        </div>
        <div className="nfts">
            <div className="inventory">
                {
                    ownedTokenIds ? ownedTokenIds.map(tokenId => <p>{tokenId}</p>) : <></>
                }
            </div>
            <div className="nft-detail">nft-detail</div>
        </div>

    </>
}

export default Collection;