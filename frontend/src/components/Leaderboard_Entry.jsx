import { react, useEffect, useState } from 'react';
import "./Leaderboard_Entry.css";

function Leaderboard_Entry(props) {
    // props: { user_name: "string", score: int }
    var user_name = props.props.user_name;
    var score = props.props.score;
    var total_guesses = props.props.total_guesses;
    var avg_off_by = props.props.avg_off_by;
    var percentage = parseInt(score / total_guesses * 100);
    console.log(user_name, score, total_guesses, percentage);
    //{user_name}: {score} / {total_guesses} ({percentage}%)
    return (
        <li>
            <p className="leaderboard-username">{user_name}</p>
            <p className="leaderboard-score">{score} / {total_guesses} ({percentage}%) {avg_off_by}</p>
        </li>
    )
}

export default Leaderboard_Entry;