// @ts-ignore

/* eslint-disable */
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://192.168.50.39:8888',
  timeout: 1000,
  // headers: {'X-Custom-Header': 'foobar'}
});

export async function getCollection(collectionId) {
  return instance.get(`/collections/${collectionId}`);
}

export async function getCollectionReport(collectionId) {
  return instance.get(`/collections/${collectionId}/report`);
}

export async function getCollectionss(collectionId) {
  return instance.get(`/collections/${collectionId}`);
}
