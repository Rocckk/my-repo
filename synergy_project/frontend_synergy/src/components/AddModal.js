import React from 'react';

class AddModal extends React.Component{
    constructor(){
        super();
        this.state = {
            new_user: null,
            new_group: null
        };
        this.send_values = this.send_values.bind(this);
        this.handleChangeUser = this.handleChangeUser.bind(this);
        this.handleChangeGroup = this.handleChangeGroup.bind(this);

    }

    render_options() {
        let options = [];
        for (let el of this.props.groups) {
            options.push(<option value={el}>{el}</option>)
        }
        return options
    }

    send_values() {
        let data = [];
        data.push(this.state.new_group);
        data.push(this.state.new_user);
        this.props.values(data);

    }

    handleChangeGroup(event) {
        this.setState({new_group: event.target.value});
    }

    handleChangeUser(event) {
        this.setState({new_user: event.target.value});

    }

    render() {
        if (this.props.show) {
        return (
            <div>
                <form>
                    <p><input type="text" value={this.state.new_user} onChange={this.handleChangeUser}></input>Username</p>
                    <p><select value={this.state.new_group} onChange={this.handleChangeGroup}>
                        {this.render_options()}
                    </select></p>
                    <button onClick={this.send_values}>Add</button>
                </form>
          </div>
        )}
        return (null)

    }

}

export default AddModal;