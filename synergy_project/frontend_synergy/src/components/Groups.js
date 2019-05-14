import React from 'react';
import axios from 'axios';
import '../App.css';
import AddGroup from './AddGroup';
import Modal from "react-modal";

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

class Groups extends React.Component {
    constructor() {
        super();
        this.state = {
            groups: [],
            show_modal: false,
            show_react_modal: false,
            group_id: null,
            new_group_name:null,
            new_descr: null

        };
        this.open_modal = this.open_modal.bind(this);
        this.edit_group = this.edit_group.bind(this);
        this.open_react_modal = this.open_react_modal.bind(this);
        this.close_react_modal = this.close_react_modal.bind(this);
        this.handleChangeGroupName = this.handleChangeGroupName.bind(this);
        this.handleChangeDescr = this.handleChangeDescr.bind(this)
    }

    componentDidMount() {
        this.get_groups()
    }

    get_groups() {
        axios.get('http://127.0.0.1:8000/groups')
            .then(result=> this.setState({groups: result.data})
            )
            .catch(function (error) {
                console.log(error)
            });
    };

    create_group(values) {
        let form_data = new FormData();
        form_data.append("group", values[0]);
        form_data.append("description", values[1]);
        axios.post("http://127.0.0.1:8000/add_group/", form_data)
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    };

    edit_group(event) {
        let form_data = new FormData();
        form_data.append("id", this.state.group_id);
        form_data.append("name", this.state.new_group_name);
        form_data.append("description", this.state.new_descr);
        axios.put("http://127.0.0.1:8000/edit_group/", form_data)
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    }

    delete_group(event) {
        let val = event.target.value;
        let form_data = new FormData();
        form_data.append("id", val);
        axios.delete("http://127.0.0.1:8000/delete_group/", {data:form_data})
            .then(result => console.log(result))
            .catch(function (error) {
                console.log(error)
            });
    };

    open_modal() {
        this.setState({show_modal: true})

    }

    open_react_modal(event) {
        this.setState({show_react_modal: true});
        this.setState({group_id: event.target.value});
    }

    close_react_modal() {
        this.setState({show_react_modal: false})
    }

    handleChangeGroupName(event) {
        this.setState({new_group_name: event.target.value});

    }

    handleChangeDescr(event) {
        this.setState({new_descr: event.target.value});
    }

    renderTable = () => {
        let table = [];
        let data = this.state.groups;
        // Outer loop to create parent
        for (let i in this.state.groups) {
            let raws = [];
            //Inner loop to create children
            raws.push(<td>{data[i].id}</td>);
            raws.push(<td>{data[i].name}</td>);
            raws.push(<td>{data[i].description}</td>);
            raws.push(<td><button value={data[i].id} onClick={this.open_react_modal}>Edit</button>
                <button onClick={this.delete_group} value={data[i].id}>Delete</button></td>);
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
                        <th>Name</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                    {this.renderTable()}
                </table>
                <button className="add" onClick={this.open_modal}>Add group </button>
                <AddGroup show={this.state.show_modal} values={this.create_group}>
                </AddGroup>
                <hr/>
                <Modal isOpen={this.state.show_react_modal}
                       onRequestClose={this.close_react_modal} style={customStyles}
                       contentLabel="Edit group">
                    <form>
                        <p><input type="text" value={this.state.new_group_name} onChange={this.handleChangeGroupName}></input>Group name</p>
                        <p><input type="text" value={this.state.new_descr} onChange={this.handleChangeDescr}></input>Description</p>
                        <button onClick={this.edit_group}>Edit</button>
                    </form>
                    <button onClick={this.close_react_modal}>close</button>
                </Modal>
            </div>
        )
    }
}

export default Groups;