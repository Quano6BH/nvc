// @ts-ignore

/* eslint-disable */
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000/api',
  // timeout: 60000,
  // headers: {'X-Custom-Header': 'foobar'}
});
const mockDate = localStorage.getItem("mockDate");

export async function getCollection(collectionId) {
  let url = `/collections/${collectionId}`;
  return instance.get(url);
}

export async function getCollectionReport(collectionId, jwt, datetime) {
  let url = `/collections/${collectionId}/report?resetCache=true`;
  if (datetime)
    url += `&datetime=${datetime.toISOString().substring(0, 10)}`
  return instance.get(url, {
    headers: { "Authorization": `Bearer ${jwt}` }
  });
}

export async function getNftDetailOfWallet(collectionId, tokenId, walletAddress, datetime) {
  let url = `/wallets/${walletAddress}/nft-detail?tokenId=${tokenId}&collectionId=${collectionId}`;
  if (datetime)
    url += `&datetime=${datetime.toISOString().substring(0, 10)}`
  return instance.get(url);
}

export async function getWalletCollectionInfo(walletAddress, collectionId, datetime) {
  let url = `wallets/${walletAddress}/collections/${collectionId}`;
  if (datetime)
    url += `?datetime=${datetime.toISOString().substring(0, 10)}`
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