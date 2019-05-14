import React from 'react';

class Modal extends React.Component{
    constructor() {
        super()
    }
    render() {
        return (
            <div>
             <p><input type="text"/>Username</p>
             <p><select>Group</select></p>
          </div>        )
    }
}
// import axios from 'axios';
// import '../App.css';
//
// const Modal = ({ show }) => {
//     if (this.show) {
//         return (
//             <div>
//                 <p><input type="text"/>Username</p>
//                 <p><select>Group</select></p>
//             </div>
//         )
//     }
// };
export default Modal;