// @ts-ignore

/* eslint-disable */
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://64.227.70.163/api',
  // timeout: 60000,
  // headers: {'X-Custom-Header': 'foobar'}
});
const mockDate = localStorage.getItem("mockDate");

export async function getCollection(collectionId) {
  let url = `/collections/${collectionId}`;
  return instance.get(url);
}

export async function getCollectionReport(collectionId, jwt) {
  let url = `/collections/${collectionId}/report`;
  if (mockDate)
    url += `?snapshotDate=${mockDate}`
  return instance.get(url, {
    headers: { "Authorization": `Bearer ${jwt}` }
  });
}

export async function getNftDetail(collectionId, tokenId, walletAddress) {
  let url = `/collections/${collectionId}/nfts/${tokenId}?walletAddress=${walletAddress}`;
  return instance.get(url);
}
export async function getNftDetailCurrent(collectionId, tokenId, walletAddress) {
  let url = `/collections/${collectionId}/nfts/${tokenId}/current?walletAddress=${walletAddress}`;
  if (mockDate)
    url += `&snapshotDate=${mockDate}`
  return instance.get(url);
}
export async function getWallet(walletAddress, collectionId = 3) {
  let url = `collections/${collectionId}/wallets/${walletAddress}`;
  if (mockDate)
    url += `?snapshotDate=${mockDate}`
  return instance.get(url);
}


export async function requestAuthenticate(walletAddress) {
  let url = `/authenticate/request`;
  return instance.post(url, {
    wallet: walletAddress
  });
}

export async function authenticate(walletAddress, signature) {
  let url = `/authenticate`;
  return instance.post(url, {
    wallet: walletAddress,
    signature: signature
  });
}

export async function updateKyc(data, jwt) {
  let url = `/wallets`;
  return instance.patch(url, data, {
    headers: { "Authorization": `Bearer ${jwt}` }
  });
}