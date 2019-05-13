import React from 'react';
import { Link } from 'react-router-dom'

class Header extends React.Component {
    render() {
        return (
            <div>
                <p><Link to='/users'>Users</Link></p>
                <p><Link to='/groups'>Groups</Link></p>
            </div>
        )
    }
}

export default Header;