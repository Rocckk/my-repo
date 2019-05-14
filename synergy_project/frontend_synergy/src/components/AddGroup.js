import React from 'react';

class AddGroup extends React.Component{
    constructor(){
        super();
        this.state = {
            new_descr: null,
            new_group: null
        };
        this.send_values = this.send_values.bind(this);
        this.handleChangeDescr = this.handleChangeDescr.bind(this);
        this.handleChangeGroup = this.handleChangeGroup.bind(this);

    }

    send_values() {
        let data = [];
        data.push(this.state.new_group);
        data.push(this.state.new_descr);
        this.props.values(data);

    }

    handleChangeGroup(event) {
        this.setState({new_group: event.target.value});
    }

    handleChangeDescr(event) {
        this.setState({new_descr: event.target.value});

    }

    render() {
        if (this.props.show) {
        return (
            <div>
                <form>
                    <p><input type="text" value={this.state.new_descr} onChange={this.handleChangeDescr}></input>Description</p>
                    <p><input type="text" value={this.state.new_group} onChange={this.handleChangeGroup}></input>Group name</p>
                    <button onClick={this.send_values}>Add</button>
                </form>
            </div>
        )}
        return (null)

    }

}

export default AddGroup;