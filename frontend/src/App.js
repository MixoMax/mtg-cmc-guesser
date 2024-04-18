// React App component
// Magic: The Gathering card mana cost guesser

import { useEffect, useState } from 'react';
import './App.css';
import MTG_Card from './components/Mtg_Card';

function App() {
  const [card_obj, setCardObj] = useState({});
  const [user_name, setUserName] = useState('');
  const [cmc_guess, setCmcGuess] = useState(0);
  const [show_correct, setShowCorrect] = useState(-1);

  useEffect(() => {
    get_random_card();
  }, []);

  function get_random_card() {
    var url = "/random_card";
    fetch(url)
      .then(response => response.json())
      .then(data => {
        setCardObj(data);
      });
  }

  function make_guess() {
    var url = "/guess?user_name=" + user_name + "&cmc_correct=" + card_obj.cmc + "&cmc_guess=" + cmc_guess;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data);
      });
    setShowCorrect(card_obj.cmc);
  }

  function make_guess_and_get_new_card() {
    make_guess();
    get_random_card();
    // clear the guess input
    setCmcGuess(0);
    document.getElementById("cmc-guess").value = "";
  }

  return (
    <div className="App">
      <h1>Magic: The Gathering Card Mana Cost Guesser</h1>
      <h2>Enter your name:</h2>
      <input type="text" value={user_name} onChange={e => setUserName(e.target.value)} />

      <br />
      <MTG_Card card_obj={card_obj} />

      <h2>Guess the converted mana cost (CMC) of the card:</h2>
      <input type="number" value={cmc_guess} onChange={e => setCmcGuess(e.target.value)} id="cmc-guess" onKeyPress={e => e.key === 'Enter' ? make_guess_and_get_new_card() : null} />

      <br />

      <button onClick={get_random_card}>Get Random Card</button>
      <button onClick={make_guess_and_get_new_card}>Make Guess and Get New Card</button>

      <br />

      <div>
        <p>Guessed: {cmc_guess}</p>
        <p>Correct: {show_correct}</p>
      </div>

      

    </div>
  );
}

export default App;