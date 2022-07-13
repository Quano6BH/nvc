import { useEffect, useContext } from 'react';
import { GlobalContext } from '../contexts/GlobalContext';
import './App.css';
import Header from './header';
import Main from './main';
import { loadWeb3 } from '../contracts'
import { getCollection } from '../apis/nvcApi'
const App = () => {
  const { setConnectedWallet, connectedWallet, setCollection } = useContext(GlobalContext);
  const collectionId = 3;
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
      setCollection(rs.data)
    })
  }, [collectionId])

  return (
    <>
      <Header />
      <Main collectionId={collectionId} />
      <footer>

      </footer>
    </>
  );
}

export default App;
