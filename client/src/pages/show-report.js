import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router'
import {Link} from 'react-router-dom';

function ShowReport() {
  const [data, setData] = useState([{}])
  const location = useLocation();
  const group = location.state
  useEffect(() => {
    fetch(`/api/report/${group}`).then(
        res => res.json()
    ).then(
        data => {
            setData(data)
            console.log(data)
        }
    )
  })
  return (
    <div>
        <h1>Report</h1>
        {(typeof data.report === 'undefined') ? (
            <p>Loading...</p>
        ): (
            data.report.map((bill, i) => (
                <p key={i}>{bill}</p>
            ))
        )}
        <br/>
        <Link to="/">
            <button>Main Menu</button>
        </Link>
    </div>
    
  )
}

export default ShowReport