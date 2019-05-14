import React from 'react';
import axios from 'axios';
import '../App.css';
import AddModal from './AddModal';
import Modal from 'react-modal';

const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};
Modal.setAppElement('#root');

class Users extends React.Component {
    constructor() {
        super();
        this.state = {
            users: [],
            user_id: null,
            show_modal: false,
            show_react_modal: false,
            new_username: null,
            new_group: null
        };
        this.delete_user = this.delete_user.bind(this);
        this.open_modal = this.open_modal.bind(this);
        this.open_react_modal = this.open_react_modal.bind(this);
        this.close_react_modal = this.close_react_modal.bind(this);
        this.handleChangeUsername = this.handleChangeUsername.bind(this);
        this.handleChangeGroup = this.handleChangeGroup.bind(this);
        this.edit_user = this.edit_user.bind(this)

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

    get_all_groups() {
        let groups = [];
        for (let el of this.state.users) {
            groups.push(el.group)
        }
        return groups
    }


    create_user(values) {
        let form_data = new FormData();
        form_data.append("group", values[0]);
        form_data.append("username", values[1]);
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
        axios.delete("http://127.0.0.1:8000/delete_user/", {data:form_data})
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    };

    edit_user(event) {
        let form_data = new FormData();
        form_data.append("id", this.state.user_id);
        form_data.append("username", this.state.new_username);
        form_data.append("group", this.state.new_group);
        axios.put("http://127.0.0.1:8000/edit_user/", form_data)
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    }

    handleChangeUsername(event) {
        this.setState({new_username: event.target.value});

    }

    handleChangeGroup(event) {
        this.setState({new_group: event.target.value});
    }

    open_modal() {
        this.setState({show_modal: true});
    }

    open_react_modal(event) {
        this.setState({show_react_modal: true});
        this.setState({user_id: event.target.value});
    }


    close_react_modal() {
        this.setState({show_react_modal: false})
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
            raws.push(<td><button value={data[i].id} onClick={this.open_react_modal}>Edit</button> <button onClick={this.delete_user} value={data[i].id}>Delete</button> </td>);
            table.push(<tr>{raws}</tr>);

        }
        return table
    };

    render_options() {
        let options = [];
        for (let el of this.get_all_groups()) {
            options.push(<option value={el}>{el}</option>)
        }
        return options
    }

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
                <AddModal show={this.state.show_modal} groups={this.get_all_groups()} values={this.create_user}>
                </AddModal>
                <hr/>
                <Modal isOpen={this.state.show_react_modal}
                       onRequestClose={this.close_react_modal} style={customStyles}
                       contentLabel="Edit user">
                    <form>
                        <p><input type="text" value={this.state.new_username} onChange={this.handleChangeUsername}></input>Username</p>
                        <p><select value={this.state.new_group} onChange={this.handleChangeGroup}>
                            {this.render_options()}
                        </select>Group</p>
                        <button onClick={this.edit_user}>Edit</button>
                    </form>
                    <button onClick={this.close_react_modal}>close</button>
                </Modal>
            </div>
        )
    }
}

export default Users;