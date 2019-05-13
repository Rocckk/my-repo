import React, { Component } from 'react';
import './App.css';
import Header from "./components/Header";
import Routs from "./components/Routs";

class App extends Component {
  render() {
    return (
      <div class="App">
          <Header />
          <Routs />
      </div>
    );
  }
}

export default App;
