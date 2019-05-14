import React from 'react';
import axios from 'axios';
import '../App.css';
import Modal from './Modal';


class Groups extends React.Component {
    constructor() {
        super();
        this.state = {
            groups: [],
            show_modal: false
        }
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

    open_modal() {
        this.setState({show_modal: true})

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
            raws.push(<td><button>Edit</button><button>Delete</button></td>);
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
                {/*<Modal show={this.state.show_modal}>*/}
                {/*</Modal>*/}
            </div>
        )
    }
}

export default Groups;