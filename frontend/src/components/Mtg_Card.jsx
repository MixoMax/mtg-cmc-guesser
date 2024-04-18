// React Magic: The Gathering card display component

import { useEffect, useState } from 'react';
import './MTG_Card.css';

// input: card_obj: {type: str, text: str, power: int | null, toughness: int | null, loyalty: int | null, cmc: int}
// displays everything except cmc

function MTG_Card({ card_obj }) {
  return (
    <div>
        <div className="card-container">
            <p id="card-type">{card_obj.type}</p>
            <p id="card-text">{card_obj.text}</p>
            <p id="card-power-toughness-loyalty">
                {card_obj.power !== null ? card_obj.power + "/" + card_obj.toughness : ""}
                {card_obj.loyalty !== null ? card_obj.loyalty : ""}
            </p>
        </div>
    </div>
  );
}


export default MTG_Card;