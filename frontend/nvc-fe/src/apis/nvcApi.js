// @ts-ignore

/* eslint-disable */
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 1000,
  // headers: {'X-Custom-Header': 'foobar'}
});

export async function getCollection(collectionId) {
  return instance.get(`/collections/${collectionId}`);
}

export async function getCollectionReport(collectionId) {
  return instance.get(`/collections/${collectionId}/report`);
}

export async function getNftDetail(collectionId, tokenId, walletAddress) {
  return instance.get(`/collections/${collectionId}/nfts/${tokenId}?walletAddress=${walletAddress}&snapshotDate=2022-07-10`);
}

export async function getWallet(walletAddress) {
  return instance.get(`/wallets/${walletAddress}`);
}
