import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Groups from './Groups';
import Users from './Users';

class Routs extends React.Component {
    render() {
        return (
            <Switch>
                <Route exact path='/' component={Users}/>
                <Route path='/users' component={Users}/>
                <Route path='/groups' component={Groups}/>
            </Switch>
        )
    }
}

export default Routs;