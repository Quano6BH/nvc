import { useEffect, useContext } from 'react';
import { GlobalContext } from '../contexts/GlobalContext';
import './App.css';
import Header from './header';
import Main from './main';
import { loadWeb3 } from '../contracts'
import { getCollection } from '../apis/nvcApi'
const App = () => {
  const { setConnectedWallet, setCollection } = useContext(GlobalContext);
  const collectionId = 1;
  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        setConnectedWallet(accounts[0]);
      },

    });
  })

  useEffect(() => {
    getCollection(collectionId).then(rs => {
      setCollection(rs.data)
    })
  }, [collectionId])

  return (
    <>
      <Header />
      <Main />
      <footer>

      </footer>
    </>
  );
}

export default App;
