import React from "react";
import {Link} from 'react-router-dom';

const Transaction = () => {
  return (
    <div>
        <h1>Create Transaction</h1>
        <br/>
        <Link to="/">
            <button>Main Menu</button>
        </Link>
    </div>
  );
};
  
export default Transaction