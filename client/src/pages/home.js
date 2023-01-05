import React from "react";
import {Link} from 'react-router-dom';
import Emoji from 'a11y-react-emoji'

const Home = () => {
  return (
    <div>
      <h1><Emoji symbol="🐙" label="Octopus" />Welcome To Octobot<Emoji symbol="🤖" label="Robot" /></h1>
        <Link to="/transaction">
                <button>Add a transaction</button>
        </Link>
        <br /> <br />
        <Link to="/report">
                <button>Generate Report</button>
        </Link>
    </div>
  );
};
  
export default Home