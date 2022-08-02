import { useEffect, useContext, useState } from 'react';
import { GlobalContext } from '../contexts/GlobalContext';
import './App.css';
import Header from './header';
import Main from './main';
import { loadWeb3 } from '../contracts'
import { getCollection } from '../apis/nvcApi'
import DateTimePicker from 'react-datetime-picker';
const App = () => {
  const { setConnectedWallet, connectedWallet, setCollection, datetime, setDatetime } = useContext(GlobalContext);
  const collectionId = 1;
  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        if (connectedWallet !== accounts[0]) {
          setConnectedWallet(accounts[0]);
        }
      },

    });
  })

  useEffect(() => {
    getCollection(collectionId).then(rs => {
      // console.log(rs)
      setCollection(rs.data.data)
    })
  }, [collectionId])

  return (
    <>
      <Header />
      <Main collectionId={collectionId} />
      <footer>

        <div className='datetime-input'>
          Date:
          <DateTimePicker onChange={setDatetime} value={datetime} />
        </div>
      </footer>
    </>
  );
}

export default App;
