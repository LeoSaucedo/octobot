import React, { useState } from "react";
import { Link } from 'react-router-dom';

// const Transaction = () => {
//     return (
//         <div>
//             <h1>Create Transaction</h1>
//             <br/>
//             <Link to="/">
//                 <button>Main Menu</button>
//             </Link>
//         </div>
//     );
// };

// export default Transaction

function Transaction() {
    const [formFields, setFormFields] = useState([
        { Group: '', Payer: '', Subtotal: '', Tax: '', Tip: '', Memo: '', Participants: []},
    ])

    const handleFormChange = (event, index) => {
        let data = [...formFields];
        data[index][event.target.name] = event.target.value;
        setFormFields(data);
    }

    const submit = (e) => {
        e.preventDefault();
        console.log(formFields)
    }

    const addFields = () => {
        let object = {
            Participant: ''
        }

        setFormFields([...formFields, object])
    }

    const removeFields = (index) => {
        let data = [...formFields];
        data.splice(index, 1)
        setFormFields(data)
    }

    return (
        <div className="App">
            <form onSubmit={submit}>

                {formFields.map((form, index) => {
                    return (
                        <div key={index}>
                            <input
                                name='Group'
                                placeholder='Group'
                                onChange={event => handleFormChange(event, index)}
                                value={form.Group}
                            />
                            <input
                                name='Payer'
                                placeholder='Payer'
                                onChange={event => handleFormChange(event, index)}
                                value={form.Payer}
                            />
                            <input
                                name='Subtotal'
                                placeholder='Subtotal'
                                onChange={event => handleFormChange(event, index)}
                                value={form.Subtotal}
                            />
                            <input
                                name='Tax'
                                placeholder='Tax'
                                onChange={event => handleFormChange(event, index)}
                                value={form.Tax}
                            />
                            <input
                                name='Tip'
                                placeholder='Tip'
                                onChange={event => handleFormChange(event, index)}
                                value={form.Tip}
                            />
                            <button onClick={() => removeFields(index)}>Remove</button>
                        </div>
                    )
                })}
            </form>
            <button onClick={addFields}>Add Participant</button>
            <br />
            <button onClick={submit}>Submit</button>
        </div>
    );
}

export default Transaction;