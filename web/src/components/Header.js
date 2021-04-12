// Dit is de header boven aan de pagina. Dit gewoon een simpele html div in een header.
import styles from './Header.module.css';
import logo from '../favicon.png'
function Header() {
  return (
    <header>
      <div className={styles.headerLogo}><img src={logo} width={25}/><h3>AgePrediction</h3></div>
    </header>
  );
}

export default Header;
