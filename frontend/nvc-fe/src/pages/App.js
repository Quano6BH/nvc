import { useEffect, useContext } from 'react';
import { GlobalContext } from '../contexts/GlobalContext';
import './App.css';
import Header from './header';
import Main from './main';
import Announcement from './announcement';
import { loadWeb3 } from '../contracts'
import { getCollection } from '../apis/nvcApi'
const App = () => {
  const { setConnectedWallet, connectedWallet, setCollection } = useContext(GlobalContext);
  const collectionId = 3;
  useEffect(() => {
    console.log("useEffect loadWeb3")
    loadWeb3({
      onAccountChanged: (accounts) => {
        console.log("loadWeb3", accounts[0], connectedWallet)
        if (connectedWallet != accounts[0]) {
          console.log("change", accounts[0], connectedWallet)
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
      <Main />
      <footer>

      </footer>
    </>
  );
}

export default App;
