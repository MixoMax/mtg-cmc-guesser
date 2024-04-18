
import { react, useEffect, useState } from 'react';
import Leaderboard_Entry from './Leaderboard_Entry';
import './Leaderboard.css';

function Leaderboard({ leaderboard_data }) {
    // props: { leaderboard_data: [ { user_name: "string", score: int }, ... ] }

    const leaderboard_entries = leaderboard_data.map((entry) => {
        return (
            <Leaderboard_Entry props={entry} />
        )
    })

    return (
        <ol>
            {leaderboard_entries}
        </ol>
    )
}

export default Leaderboard;