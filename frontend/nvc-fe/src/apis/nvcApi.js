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
