import React, {useState} from "react";
import {useNavigate, Link} from 'react-router-dom';


const Report = () => {
    const [group, setGroup] = useState('');
    const navigate = useNavigate();

    const handleOnChange = (e) => {
        e.preventDefault();
        const value = e.target.value;
        setGroup(value)
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        navigate('/show-report', {state:group})
    }
    return (
            <div>
                <h1>Generate Report</h1>
                <form onSubmit={handleSubmit}>
                    <label>
                        Group: 
                        <input type="text" value={group} onChange={handleOnChange} />
                    </label>
                    <br/><br/>
                    <input type="submit" value="Submit" />
                </form>
                <br/>
                <Link to="/">
                    <button>Main Menu</button>
                </Link>
            </div>
    );
};
  
export default Report