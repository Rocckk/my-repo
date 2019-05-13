import React from 'react';
import axios from 'axios';
import '../App.css';
import Modal from './Modal';


class Users extends React.Component {
    constructor() {
        super();
        this.state = {
            users: [],
            user_id: null,
            show_modal: false
        };
        this.delete_user = this.delete_user.bind(this);
        this.open_modal = this.open_modal.bind(this)
    }

    componentDidMount() {
        this.get_users()
    }

    get_users() {
        axios.get('http://127.0.0.1:8000/')
            .then(result=> this.setState({users: result.data})
            )
            .catch(function (error) {
                console.log(error)
            });
    };

    create_user() {
        let form_data = new FormData();
        form_data.append("group", "fialkagroup");
        form_data.append("username", "fialka");
        axios.post("http://127.0.0.1:8000/add_user/", form_data)
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    };

    delete_user(event) {
        let val = event.target.value;
        let form_data = new FormData();
        form_data.append("id", val);
        // this.setState({user_id: value}, () => {
        //     form_data.append("id", this.state.user_id);
        // });
        axios.delete("http://127.0.0.1:8000/delete_user/", {data:form_data})
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    };

    open_modal() {
        alert(this.state.show_modal);
        this.setState({show_modal: true});
        alert(this.state.show_modal, "**");


    }

    renderTable = () => {
        let table = [];
        let data = this.state.users;
        // Outer loop to create parent
        for (let i in this.state.users) {
            let raws = [];
            //Inner loop to create children
            raws.push(<td>{data[i].id}</td>);
            raws.push(<td>{data[i].username}</td>);
            raws.push(<td>{data[i].created}</td>);
            raws.push(<td>{data[i].group}</td>);
            raws.push(<td><button value={data[i].id}>Edit</button> <button onClick={this.delete_user} value={data[i].id}>Delete</button> </td>);
            table.push(<tr>{raws}</tr>);

        }
        return table
    };

    render() {
        return (
            <div>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Created</th>
                        <th>Group</th>
                        <th>Actions</th>
                    </tr>
                    {this.renderTable()}
                </table>
                <button className="add" onClick={this.open_modal}>Add user </button>
                {/*<Modal show={this.state.show_modal}>*/}
                {/*</Modal>*/}
            </div>
        )
    }
}

export default Users;