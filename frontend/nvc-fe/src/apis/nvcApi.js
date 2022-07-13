// @ts-ignore

/* eslint-disable */
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://64.227.70.163/api',
  // timeout: 60000,
  // headers: {'X-Custom-Header': 'foobar'}
});

export async function getCollection(collectionId) {
  return instance.get(`/collections/${collectionId}`);
}

export async function getCollectionReport(collectionId) {
  return instance.get(`/collections/${collectionId}/report`);
}

export async function getNftDetail(collectionId, tokenId, walletAddress) {
  return instance.get(`/collections/${collectionId}/nfts/${tokenId}?walletAddress=${walletAddress}`);
}
export async function getNftDetailCurrent(collectionId, tokenId, walletAddress) {
  return instance.get(`/collections/${collectionId}/nfts/${tokenId}/current?walletAddress=${walletAddress}`);
}
export async function getWallet(walletAddress, collectionId = 3) {
  return instance.get(`collections/${collectionId}/wallets/${walletAddress}`);
}


export async function requestAuthenticate(walletAddress) {
  return instance.post(`/authenticate/request`, {
    wallet: walletAddress
  });
}

export async function authenticate(walletAddress, signature) {
  return instance.post(`/authenticate`, {
    wallet: walletAddress,
    signature: signature
  });
}