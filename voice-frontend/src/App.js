import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Login from './Login';

class App extends Component {
    constructor(props) {
      super(props);
      this.state = {
          isLoggedIn: false
      };
    }

    checkLoggedIn = () => {
        return this.state.isLoggedIn;
    }

    invalidateSession = () => {
        return false;
    }

    handleLogin = (event, username, password) => {
        console.log(event);
        console.log(username);
        console.log(password);
        this.setState(state => ({...state, isLoggedIn: true}));
    }

  render() {
        if (this.state.isLoggedIn){
            return (
                <div>
                    You are logged in!
                </div>
            )
        }
    return (
      <div className="App">
        <Login handleSubmit={this.handleLogin}/>
      </div>
    );
  }
}

export default App;
