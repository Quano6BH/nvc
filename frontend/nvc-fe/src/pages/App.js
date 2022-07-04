import { useEffect, useContext } from 'react';
import { GlobalContext, GlobalContextProvider } from '../contexts/GlobalContext';
import './App.css';
import Header from './header';
import Main from './main';
import { loadWeb3 } from '../contracts'
const App = () => {
  const { setConnectedWallet } = useContext(GlobalContext);
  useEffect(() => {
    loadWeb3({
      onAccountChanged: (accounts) => {
        setConnectedWallet(accounts[0]);
      },

    });

  })
  return (
    <GlobalContextProvider>

      <Header />
      <Main />
      <footer>

      </footer>
    </GlobalContextProvider>
  );
}

export default App;
