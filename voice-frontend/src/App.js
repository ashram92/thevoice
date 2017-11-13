import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Login from './Login';
import axios from 'axios';
import Cookies from 'universal-cookie';

const BASE_URL = ''; // 'http://127.0.0.1:8000';
const LOGIN_URL = BASE_URL + '/accounts/api/login/';
const LOGOUT_URL = BASE_URL + '/accounts/api/logout/';
const PROFILE_URL = BASE_URL + '/accounts/api/profile/';


class App extends Component {
    constructor(props) {
        super(props);
        this.cookie = new Cookies();
        this.state = {
            isLoggedIn: this.checkLoggedIn()
        };
    }

    checkLoggedIn = () => {
        if (this.cookie.get('loggedIntoVoice') === '1') {
            return true;
        }
        return false;
    }

    setLoggedIn = () => {
        this.cookie.set('loggedIntoVoice', '1');
        this.setState(state => ({...state, isLoggedIn: true}));
    }

    invalidateSession = () => {
        this.cookie.remove('loggedIntoVoice');
        this.setState(state => ({...state, isLoggedIn: false}));
    }

    handleLogin = (event, username, password) => {
        axios.post(LOGIN_URL, {
            username: username,
            password: password,
        }).then(response => {
            this.setLoggedIn();
        }).catch(error => {
            this.invalidateSession();
            alert('Bad login details!');
        });
    }

    handleLogout = (event) => {
        axios.get(LOGOUT_URL).then(
            response => {
                return this.invalidateSession();
            }
        ).catch(
            error => {
                return this.invalidateSession();  // Fallback to logging out.
            }
        );
    }

  render() {
        if (this.checkLoggedIn()){
            return (
                <div>
                    You are logged in!
                    <button onClick={this.handleLogout}>Logout</button>
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
